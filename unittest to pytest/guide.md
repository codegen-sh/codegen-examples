# Guide: Migrating from Unittest to Pytest with Codegen

This guide walks you through the steps to migrate your codebase from Unittest to Pytest using Codegen. Follow along to decouple your test cases from the Unittest framework and transform your setup methods into Pytest fixtures. Each step includes a direct link to the appropriate codemod for easy implementation.

---

## 🎉 Overview of Changes

The migration focuses on these key updates:

1. **Remove Unittest Inheritance**  
   This codemod iterates through files in the tests directory and removes inheritance from `unittest.TestCase` for classes that have it. This helps in decoupling test cases from the Unittest framework, potentially preparing them for migration to another testing framework like Pytest.  
   [Run the Remove Unittest Inheritance Codemod](https://www.codegen.sh/preview/6867)

2. **Transform setUp Methods to Pytest Fixtures**  
   This codemod transforms `setUp` methods in unit tests into Pytest fixtures, adding necessary imports and creating fixture functions. It updates test methods to utilize these fixtures, removes obsolete `setUp` methods, and eliminates Unittest imports, ensuring a seamless transition from Unittest to Pytest.  
   [Run the Transform setUp Methods Codemod](https://www.codegen.sh/preview/6919)

---

## How to Migrate

### Step 1: Remove Unittest Inheritance

Use the codemod to remove inheritance from `unittest.TestCase` in your test classes. This will help decouple your test cases from the Unittest framework.

👉 [Run the Remove Unittest Inheritance Codemod](https://www.codegen.sh/preview/6867)

### Step 2: Transform setUp Methods to Pytest Fixtures

Use the codemod to transform `setUp` methods into Pytest fixtures. This includes adding necessary imports, creating fixture functions, updating test methods to use these fixtures, and removing obsolete `setUp` methods and Unittest imports.

👉 [Run the Transform setUp Methods Codemod](https://www.codegen.sh/preview/6919)

---

## Need Help?

If you encounter issues or have specific edge cases not addressed by the codemods, reach out to the Codegen support team or visit the [Codegen Documentation](https://www.codegen.sh/docs) for detailed guidance.

Start your Pytest migration today and enjoy the benefits of a cleaner, modern codebase!
