from contextlib import contextmanager
from threading import Lock
from typing import Final, Iterator

from Autumn.Naming.class_ import Class
from Autumn.Naming.identifier import Identifier


class Generator:
    """
    Used for generating Identifiers and Classes. It's recommended to use the context
    Generator.context(...) for one-time used instances.

    This class is responsible only for generating the identifiers/classes. The only thing that actually
    makes them unique is your prefixes/suffixes.

    Please note that using this for any security purposes is worse practice, instead,
    use secrets.token_urlsafe or secrets.token_hex,
    """

    @classmethod
    @contextmanager
    def context(cls, *, prefix: str = "", suffix: str = "") -> Iterator["Generator"]:
        yield Generator(prefix=prefix, suffix=suffix)

    def __init__(self, *, prefix: str = "", suffix: str = "") -> None:

        self._lock = Lock()

        self._prefix: str = prefix
        self._suffix: str = suffix

        self._defined_identifiers: set[str] = set()
        self._defined_classes: set[str] = set()

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        uppercase_alphabet = alphabet.upper()
        numbers = "0123456789"

        self._class_pointers: list[int] = [0]
        self._identifier_pointers: list[int] = [0]

        self._identifier_incrementing_map: list[bool] = [True]
        self._class_incrementing_map: list[bool] = [True]

        self._first_letter: Final[str] = alphabet + uppercase_alphabet
        self._charset: Final[str] = alphabet + uppercase_alphabet + numbers + "-_"

    def generate_identifier(self, *, raw: bool = True) -> str | Identifier:
        """
        Generates an identifier. The stored identifier is unique to this instance.

        :param raw: Whether to return str(raw) or identifier(made).
        :return: A string or Identifier object.
        """
        with self._lock:
            out = self._prefix + self._generate(self._defined_identifiers, self._identifier_pointers,
                                                self._identifier_incrementing_map) + self._suffix
        if raw:
            return out
        return Identifier(out)

    def generate_class(self, *, raw: bool = True) -> str | Class:
        """
        Generates a class. The stored class is unique to this instance.

        :param raw: Whether to return str(raw) or class(made).
        :return: A string or Class object.
        """
        with self._lock:
            out = self._prefix + self._generate(self._defined_classes, self._class_pointers,
                                                self._class_incrementing_map) + self._suffix
        if raw:
            return out
        return Class(out)

    def reset(self, *, prefix: str | None = None, suffix: str | None = None) -> None:
        """
        Resets the prefix and suffix.

        :param prefix: The new prefix to use.
        :param suffix: The new suffix to use.
        """
        if not (prefix is not None or suffix is not None):
            return
        with self._lock:
            if prefix is not None:
                self._prefix = prefix
            if suffix is not None:
                self._suffix = suffix

    def _generate(self, predefined: set[str], pointers: list[int], incr: list[bool], /) -> str:
        approved = False

        max_first_position = len(self._first_letter) - 1
        max_position = len(self._charset) - 1

        charset = self._charset
        first_letter = self._first_letter

        returning = ""

        while not approved:

            # Generating
            out = [first_letter[pointers[0]]]
            for pointer in pointers[1:]:
                out.append(charset[pointer])
            made = "".join(out)

            # Approving
            if made not in predefined:
                returning = made
                approved = True
                # continue missing to prevent re-checking on next run.

            # Changing pointers

            ## If all pointers are maxed out, add a new pointer and reset all.
            if all(pointer == max_position for pointer in pointers[1:]) and pointers[0] == max_first_position:
                for i in range(len(pointers)):
                    pointers[i] = 0
                pointers.append(0)
                incr[0] = True
                incr.append(False)
                for i in range(1, len(pointers)):
                    incr[i] = False
                continue

            ## If not, find the first incrementing and increase it.
            ## Some patterns may be skipped, due to how it works,
            ## But it's already good enough, as it's not expensive and
            ## It covers many patterns.

            done_increasing = False
            last_index = 0

            while not done_increasing:

                if True in incr[last_index:]:
                    index = incr.index(True, last_index)
                    pointer = pointers[index]

                    if index != 0 and pointer < max_position:
                        pointers[index] += 1
                        done_increasing = True
                        continue
                    elif index == 0 and pointer < max_first_position:
                        pointers[index] += 1
                        done_increasing = True
                        continue
                    else:
                        last_index = index + 1
                        continue
                if incr[-1]:  # Checks whether the last position was active,
                    # which means this is the last possibility we can get.
                    trues = incr.count(True) + 1
                    for i in range(len(incr)):
                        if trues != 0:
                            incr[i] = True
                            trues -= 1
                        else:
                            incr[i] = False
                    for pointer_index in range(len(pointers)):
                        pointers[pointer_index] = 0
                else:
                    incr.insert(0, incr.pop())
                    for pointer_index in range(len(pointers)):
                        pointers[pointer_index] = 0

                done_increasing = True

        predefined.add(returning)

        return returning
