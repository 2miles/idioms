## Scrape the examples

## Manually acquire all the examples that the scraper didnt get

## Clean the results

- Manulally Identify all the single quotes that are actually going to be nested quotes and convert them to (backslash double-quote).
- Convert all the remaining single quotes to literal 'RIGHT SINGLE QUOTATION MARK' `option + shift + ]` `%s/'/’/g`
- Convert all `\u2019` to literal 'RIGHT SINGLE QUOTATION MARKS' `%s/\\u2019/’/g`
- Convert all RIGHT and LEFT DOUBLE QUOTATION MARK to escaped double quotes
- Manually convert all relevant `\u2018` , 'LEFT SINGLE QUOTE' and `\u2019` 'RIGHT SINGLE QUOTE' to escaped double quotes
- Convert all relevant dashes to EM DASH if needed
- Convert all `\u2026` to `...`
- Convert all `\u2013`, 'EN DASH' to `-`
- Fix any spelling errors
- Remove any doubles
- Remove any trailing whitespace

“ Left double quotation mark
option + [

” Right double quotation mark
option + shift + [

‘ Left single quotation mark
option + ]

’ Right single quotation mark
option + shift + ]

## Where to find origins:

- poemanalysis.com
- wordhistories.net, Creative Commons
