# Info

Types:
* Adding Tests - Used for TODOs that include adding a test - fields: Minimum tests - The minimum number of tests to add.
* Feature - Used for TODOs that add a new feature, whether to fix another class's problems or a complete new feature - fields: None
* Breaking Feature - Used for TODOs that add a breaking feature that replaces another feature or somehow breaks something - fields: None

# Undone

## Increase the tests including autoinit feature.
* Description:
  ```text
  The tests for autoinit cover minimum edge cases.
  Add tests for other edge cases, even a dedicated file for
  AbstractBase features sounds good.
  ```
* Type: Adding Tests
* Minimum tests: 2

## Get famous
* Description:
  ```text
  For a while, I'm going to work on other things(nerina0coder-star), and I will be absent.
  In my absence, I hope the framework grows well, some people see it, and so.
  ```
* Type: ?

## Global usable generator
* Description:
  ```text
  The current generator, while fast, consumes a lot of memory for storing pointers and state.
  Create a new generator that fixes that problem.
  ```
* Type: Feature

## CSS Selectors
* Description:
  ```text
  Selectors play a huge role in CSS, and Autumn(Core) can't implement everything.
  Add a new class, e.g., Selector, that users can define and use, and so the framework
  won't limit them.
  ```
* Type: Breaking Feature

## CSS Sorting and Ordering mechanisms
* Description:
  ```text
  One of the most long-lived problems with CSS is the C, Cascade.
  How Autumn will handle this is by using a worth mechanisms that orders
  each style in a sheet, therefore taking the most important ones to the bottom(so it overrides
  the top) and the less important to the top(so it's the first overriden).
  An idea is that the styles can hold any integer-able value, such as an Enum that defines __int__,
  then the styles will be sorted via sorted(styles) where styles is the list of styles.
  ```
* Type: Feature

# Done
Not any yet

# Cancelled

## CSS Selectors need update
* Description:
  ```text
  Current CSS selectors cover bare minimum of what CSS is capable of.
  Please add new CSS selectors, such as ~ * >, etc... and in the Attribute Selector,
  |=, i, ~=, and so on.
  ```
* Type: Feature
