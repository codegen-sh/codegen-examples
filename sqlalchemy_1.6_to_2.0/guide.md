# Guide: Migrating from SQLAlchemy 1.6 to 2.0 with Codegen

This guide walks you through the steps to migrate your codebase from SQLAlchemy 1.6 to 2.0 using Codegen. Follow along to modernize your imports, relationships, and query syntax while ensuring compatibility with SQLAlchemy 2.0. Each step includes a direct link to the appropriate codemod for easy implementation.

---

## 🎉 Overview of Changes

The migration focuses on these key updates:

1. **Import Adjustments**  
   Aligns your code with the updated SQLAlchemy 2.0 module structure.  
   [Run the Import Codemod](https://www.codegen.sh/search/6506?skillType=codemod)

2. **Relationship Updates**  
   Refines relationship definitions by replacing `backref` with `back_populates` for explicitness and better readability.  
   [Run the Relationship Codemod](https://www.codegen.sh/search/6510?skillType=codemod)

3. **Query Syntax Modernization**  
   Updates queries to leverage the latest syntax like `select()` and `where()`, removing deprecated methods.  
   [Run the Query Syntax Codemod](https://www.codegen.sh/search/6508?skillType=codemod)

4. **Relationship Lazy Loading**
   SQLAlchemy 2.0 introduces a new `lazy` parameter for relationship definitions. Update your relationships to use the new `lazy` parameter for improved performance.  
   [Run the Relationship Lazy Loading Codemod](https://www.codegen.sh/search/6512?skillType=codemod)

---

## How to Migrate

### Step 1: Update Imports

SQLAlchemy 2.0 introduces a refined import structure. Use the import codemod to:

- Replace wildcard imports (`*`) with explicit imports for better clarity.
- Update `declarative_base` to `DeclarativeBase`.

👉 [Run the Import Codemod](https://www.codegen.sh/search/6506?skillType=codemod)

---

### Step 2: Refactor Relationships

In SQLAlchemy 2.0, relationships require more explicit definitions. This includes:

- Transitioning from `backref` to `back_populates` for consistency.
- Explicitly specifying `back_populates` for all relationship definitions.

👉 [Run the Relationship Codemod](https://www.codegen.sh/search/6510?skillType=codemod)

---

### Step 3: Modernize Query Syntax

The query API has been revamped in SQLAlchemy 2.0. Key updates include:

- Switching to `select()` and `where()` for query construction.
- Replacing any deprecated methods with their modern equivalents.

👉 [Run the Query Syntax Codemod](https://www.codegen.sh/search/6508?skillType=codemod)

---

### Step 4: Update Relationship Lazy Loading

SQLAlchemy 2.0 introduces a new `lazy` parameter for relationship definitions. Update your relationships to use the new `lazy` parameter for improved performance.

👉 [Run the Relationship Lazy Loading Codemod](https://www.codegen.sh/search/6512?skillType=codemod)

---

## Need Help?

If you encounter issues or have specific edge cases not addressed by the codemods, reach out to the Codegen support team or visit the [Codegen Documentation](https://www.codegen.sh/docs) for detailed guidance.

Start your SQLAlchemy 2.0 migration today and enjoy the benefits of a cleaner, modern codebase!
