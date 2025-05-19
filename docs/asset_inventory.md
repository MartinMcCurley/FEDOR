# FEDOR - GTO Asset Inventory

This document catalogs the specific Game Theory Optimal (GTO) resources targeted for the FEDOR project, with a focus on preflop charts and push/fold tables for 5-max No-Limit Texas Hold'em (2-30bb effective stacks).

## 1. Preflop Charts

| Asset | Source | Stack Depth | Format | License | Status | Priority | URL |
|-------|--------|-------------|--------|---------|--------|----------|-----|
| RFI Charts (BTN) | GTO Wizard | 25bb | HTML/Screenshot | Free tier | To acquire | High | [GTO Wizard](https://gtowizard.com) |
| RFI Charts (CO) | GTO Wizard | 25bb | HTML/Screenshot | Free tier | To acquire | High | [GTO Wizard](https://gtowizard.com) |
| RFI Charts (MP) | GTO Wizard | 25bb | HTML/Screenshot | Free tier | To acquire | Medium | [GTO Wizard](https://gtowizard.com) |
| RFI Charts (SB) | GTO Wizard | 25bb | HTML/Screenshot | Free tier | To acquire | High | [GTO Wizard](https://gtowizard.com) |
| vs RFI (BB vs BTN) | GTO Wizard | 25bb | HTML/Screenshot | Free tier | To acquire | High | [GTO Wizard](https://gtowizard.com) |
| vs RFI (BB vs SB) | GTO Wizard | 25bb | HTML/Screenshot | Free tier | To acquire | High | [GTO Wizard](https://gtowizard.com) |
| 3-Bet Ranges (BB vs BTN) | Upswing Poker | 20-30bb | PDF | Free content | To acquire | Medium | [Upswing Poker](https://upswingpoker.com) |
| 4-Bet Ranges | PokerCoaching | 25bb | PDF | Free charts | To acquire | Low | [PokerCoaching](https://pokercoaching.com) |
| Scribd 25bb Charts | Scribd | 25bb | PDF | User-uploaded | To acquire | Medium | [Scribd](https://www.scribd.com/document/257466554/25bb-gto-charts) |
| Scribd 15bb Charts | Scribd | 15bb | PDF | User-uploaded | To acquire | Medium | [Scribd](https://www.scribd.com) |

## 2. Push/Fold Tables

| Asset | Source | Stack Depth | Format | License | Status | Priority | URL |
|-------|--------|-------------|--------|---------|--------|----------|-----|
| BTN Push Charts | ConsciousPoker | 5-12bb | HTML/Image | Free | To acquire | Very High | [ConsciousPoker](https://consciouspoker.com) |
| SB Push Charts | ConsciousPoker | 5-12bb | HTML/Image | Free | To acquire | Very High | [ConsciousPoker](https://consciouspoker.com) |
| CO Push Charts | ConsciousPoker | 5-12bb | HTML/Image | Free | To acquire | High | [ConsciousPoker](https://consciouspoker.com) |
| BTN vs SB Calling Ranges | SnapShove | 5-15bb | App/Screenshot | Free tier | To acquire | High | [SnapShove](https://snapshove.com) |
| SB vs BB Calling Ranges | SnapShove | 5-15bb | App/Screenshot | Free tier | To acquire | High | [SnapShove](https://snapshove.com) |
| BB Calling Ranges | FloatTheTurn | 5-12bb | App/Screenshot | Free | To acquire | High | [FloatTheTurn](https://floattheturn.com) |
| ICMIZER Open-Shove | ICMIZER Blog | 16bb | Image | Free examples | To acquire | Medium | [ICMIZER Blog](https://www.icmpoker.com/blog/) |

## 3. Academic/Other Resources

| Asset | Source | Stack Depth | Format | License | Status | Priority | URL |
|-------|--------|-------------|--------|---------|--------|----------|-----|
| SimpleNash Outputs | SimpleNash | Various | Text | Free | To acquire | Low | [SimpleNash](https://simplenash.com) |
| Cepheus Preflop | University of Alberta | N/A (Limit HE) | Web interface | Academic/Public | To acquire | Low | [Cepheus Poker](http://poker.srv.ualberta.ca/) |
| GTOBase Free Solutions | GTOBase | Various | Web interface | Free tier | To acquire | Medium | [GTOBase](https://gtobase.com) |

## 4. Acquisition Strategy

1. **Direct Downloads**: For freely available PDFs and charts (PokerCoaching, some Upswing content)
2. **Web Screenshots**: For GTO Wizard, FloatTheTurn, and other web-based tools with free access
3. **App Interaction**: For SnapShove and similar apps, create systematic screenshots of key ranges
4. **Manual Transcription**: For resources without download/screenshot options, manually record data
5. **Academic Requests**: For Cepheus and research-based resources, use available APIs or request data access

## 5. Parsing Complexity Assessment

| Source Format | Parsing Complexity | Required Tools | Notes |
|---------------|-------------------|----------------|-------|
| PDF (clean text) | Low | PyPDF2, pdfminer.six | Most structured PDFs with selectable text |
| PDF (image-based) | High | pdf2image + pytesseract OCR | Charts rendered as images require OCR |
| HTML (tables) | Medium | Beautiful Soup | Web tables often have consistent structure |
| HTML (interactive) | High | Selenium + Beautiful Soup | May require browser automation |
| Images | Very High | pytesseract, opencv | Requires image processing and OCR |
| App Screenshots | Very High | pytesseract, opencv | Requires standardized screenshot process |

## 6. Initial Data Collection Focus

For Milestone 1, focus on acquiring these specific high-priority resources:

1. GTO Wizard BTN and SB RFI charts (25bb)
2. ConsciousPoker BTN and SB push charts (5-12bb)
3. SnapShove BTN vs SB and SB vs BB calling ranges (5-15bb)
4. Scribd 25bb GTO charts PDF

These will provide sufficient coverage of the most critical preflop spots while keeping the parsing development manageable. 