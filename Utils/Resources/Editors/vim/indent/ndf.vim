" Vim indent file
" Language:     NDF
" File Types:   .ndf

" Only load this indent file when no other was loaded.
if exists("b:did_indent")
  finish
endif
let b:did_indent = 1

setlocal autoindent
setlocal indentexpr=GetNDFIndent(v:lnum)
setlocal indentkeys='0},0),0],o,O'

if exists("*GetNDFIndent")
  finish
endif

function GetNDFIndent(lnum)
  let plnum = prevnonblank(v:lnum - 1)

  if plnum == 0
    return 0
  endif

  let ind = indent(plnum)

  let p = searchpair('(\|\[', '', ')\|\]', 'bW')
  if p == plnum
    let ind = ind + &sw
  endif

  if getline(v:lnum) =~ '^\s*\()\|\]\)'
    let ind = ind - &sw
  endif

  return ind
endfunction
