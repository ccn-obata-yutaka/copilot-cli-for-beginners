---
name: book-summary
description: Create a formatted markdown summary of a book collection
---

# Book Summary Generator

Create a summary of the books following the rules:

1. Output a markdown table with columns: Title, Author, Year, Status
2. Use ☑️ for read books and ⬜ for unread books in the Status column
3. Sort the table by Year in descending order
4. Include a total count at the bottom
5. Flag any data issues (missing authors, invalid years)

Example output:
| Title                 | Author              | Year | Status |
|-----------------------|---------------------|------|--------|
| The Great Gatsby      | F. Scott Fitzgerald | 1925 |   ☑️   |
| To Kill a Mockingbird | Harper Lee          | 1960 |   ⬜   |

**Total Books: 2 (1 read, 1 unread)**