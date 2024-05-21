" Vim detection file
" Language:     NDF
" File Types:   .ndf

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if version < 600
    syntax clear
elseif exists("b:current_syntax")
    finish
endif

syn keyword ndfKeyword export is template end else elif begin const class do function for isnil inherited indexing object obj override prototype procedure protected private public package require then to var virtual with and or not div unnamed meta
syn region  ndfPreCondit start="^\s*#\s*\(ifdef\|ifndef\|else\|endif\)\>" end="$" end="//"me=s-1
syn region  ndfDefine start="^\s*#\s*\(define\|undef\)\>" skip="\\$" end="$" end="//"me=s-1
syn keyword ndfConstant true false True False nil
syn keyword ndfOperator - ! $ * , : ? ~ < = >
syn match   ndfNumber "\<\d\+\(f\|d\)\?"
syn region  ndfComment start="//" end="$"
syn region  ndfComment start="{" end="}"
syn match   ndfIdentifier "\w\+\s\+is\>"me=e-3
syn match   ndfReference "\([~$]\?\|\w\+\)\(/\w\+\)\+"
syn match   ndfType "\<\w\+\([ \t\n]\+meta\)\?[ \t\n]*[(\[]"me=e-1 contains=ndfKeyword

syn region ndfString start=+"+ skip=+$+ end=+"+
syn region ndfString start="'" skip="$" end="'"

hi def link ndfKeyword Keyword
hi def link ndfOperator Operator
hi def link ndfPreCondit PreCondit
hi def link ndfDefine Define
hi def link ndfString String
hi def link ndfConstant Constant
hi def link ndfNumber Number
hi def link ndfComment Comment
hi def link ndfIdentifier Identifier
hi def link ndfType Type
hi def link ndfReference Label

let b:current_syntax = "ndf"

