# Flow

```mermaid
flowchart TD
    A[Excel Inventory Spreadsheet] -->|Modify Column Headers| B[Export to CSV]
    B --> C[Convert to FDF]
    C --> D[Use PDFtk to populate template]
```
