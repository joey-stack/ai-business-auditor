# Google Sheet Configuration

## Spreadsheet
- Sheet ID: 1dFqr9zvJXDya30YyhERjoBYtE6o3lMFdYAhfavknAl4
- Spreadsheet URL: https://docs.google.com/spreadsheets/d/1dFqr9zvJXDya30YyhERjoBYtE6o3lMFdYAhfavknAl4/edit
- Sheet name: "Outreach Pipeline"
- Total Columns: A–R

## Column Layout

### Agent-Written Block (Contiguous, A–K):
- **A**: Business Name
- **B**: Location
- **C**: Opportunity Score
- **D**: Tier (`Tier A` | `Tier B` | `Tier C` | `Tier D`)
- **E**: Audit PDF Link
- **F**: Video Walkthrough Link
- **G**: Call Script Link
- **H**: Suggested Opening Line
- **I**: Contact Name
- **J**: Contact Title
- **K**: LinkedIn Profile URL

### User-Managed Block (Contiguous, L–R):
- **L**: Outreach Status
- **M**: Touch 1 Date
- **N**: Touch 2 Date
- **O**: Touch 3 Date
- **P**: Last Touch Result
- **Q**: Next Action
- **R**: Notes

## Write Rules
1. **Agent writes A–K only** in a single contiguous `append-rows` call.
2. **L–R are user-managed and must never be touched** by the agent under any circumstance.
3. **Always append**: Never overwrite an existing row.
4. **Blank values**: If LinkedIn URL is null or not found, leave Column K blank as part of the standard A–K write. Never omit the column or shift columns.
