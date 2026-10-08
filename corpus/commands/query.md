---
name: query
aliases: [xquery]
also_documents: [queryyes]
source: XSquery.tex
---

# query

**set a default answer for prompts in scripts**

Switch on/off the continue fitting questions.

**Syntax:** `query` <option>

where `<option>` is `yes`, `no`, or `on`.
If `on` then the continue fitting question in `fit`, `steppar`, 
and `error` will be asked when the number of trials is exceeded. 
Also, when the number of trials to find the error is exceeded a question will be asked.
For either of the other two options the questions will not be asked but the answer
will be assumed to be `yes` or `no` depending on the value set. 
To ensure that fitting continues without any questions being asked use the command:

```
XSPEC> query yes
```
