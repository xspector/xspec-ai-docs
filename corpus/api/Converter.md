---
class: Converter
module: convert.py
---

# Converter

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| source | — | instance |  |
| report | — | instance |  |
| lines | — | instance |  |
| indent | — | instance |  |
| used | — | instance |  |
| tmp | — | instance |  |
| scope | — | instance |  |
| scopes_types | — | instance |  |
| procs | — | instance |  |
| line_no | — | instance |  |
| loop_next | — | instance |  |
| exited | — | instance |  |
| cur_line | — | instance |  |
| all_bridged | — | instance |  |

## Methods

- `__init__(source)`
- `emit(text)`
- `newtmp(stem='_t')`
- `fallback(what)`
- `pyname(name)`
- `is_global_ref(name)`
- `vtype(name)`
- `note_assign(name, typ)`
- `literal(text)`
- `strlit(text)`
- `as_str(e)` — Python source for the Tcl string form of e.
- `as_num(e)`
- `as_int(e)`
- `as_list(e)`
- `as_bool(e)`
- `word(w)`
- `tokens(toks, form='bare')`
- `concat(parts)`
- `arglist(words)` — Python argument source for words, {*}word expanded.
- `token(t)`
- `varref(name, index)`
- `cmd_value(script)`
- `command_value(cmd)` — A command used for its value: an expression, hoisting any
- `body(raw, base_line, ret_last=False, assign_last=None)` — Translate a braced script (a body).  ret_last: a proc body, whose
- `statement(cmd)`
- `dispatch(words, text, value)`
- `command_string(words)` — Python source for the command line these words make, as the bridge
- `bridged(words, text, value, reason=None)`
- `shell(words, value)`
- `run_script(args, value)`
- `call_proc(name, argwords, value)`
- `target(w)` — The Python assignment target for a variable-name word.
- `tcl_set(words, text, value)`
- `tcl_unset(words, text, value)`
- `tcl_incr(words, text, value)`
- `tcl_append(words, text, value)`
- `tcl_lappend(words, text, value)`
- `tcl_global(words, text, value)`
- `expr_text(words)` — The expression source of `expr`'s argument words (several words are
- `tcl_expr(words, text, value)`
- `expr(src, ctx)`
- `cond(w)` — A condition word (if/while/for): a braced expression, or a word
- `tcl_if(words, text, value)`
- `body_word(w)`
- `tcl_while(words, text, value)`
- `tcl_for(words, text, value)`
- `tcl_foreach(words, text, value)`
- `tcl_break(words, text, value)`
- `tcl_continue(words, text, value)`
- `tcl_switch(words, text, value)`
- `tcl_proc(words, text, value)`
- `tcl_return(words, text, value)`
- `tcl_error(words, text, value)`
- `tcl_catch(words, text, value)`
- `tcl_eval(words, text, value)`
- `tcl_source(words, text, value)`
- `tcl_package(words, text, value)`
- `tcl_null(words, text, value)`
- `tcl_puts(words, text, value)`
- `tcl_open(words, text, value)`
- `tcl_close(words, text, value)`
- `tcl_flush(words, text, value)`
- `tcl_gets(words, text, value)`
- `tcl_read(words, text, value)`
- `tcl_eof(words, text, value)`
- `tcl_file(words, text, value)`
- `tcl_exec(words, text, value)`
- `tcl_cd(words, text, value)`
- `tcl_pwd(words, text, value)`
- `tcl_glob(words, text, value)`
- `tcl_after(words, text, value)`
- `tcl_clock(words, text, value)`
- `tcl_info(words, text, value)`
- `tcl_array(words, text, value)`
- `tcl_list(words, text, value)`
- `tcl_llength(words, text, value)`
- `tcl_lindex(words, text, value)`
- `tcl_lrange(words, text, value)`
- `tcl_lsort(words, text, value)`
- `tcl_lsearch(words, text, value)`
- `tcl_linsert(words, text, value)`
- `tcl_lreplace(words, text, value)`
- `tcl_lreverse(words, text, value)`
- `tcl_concat(words, text, value)`
- `tcl_join(words, text, value)`
- `tcl_split(words, text, value)`
- `tcl_lset(words, text, value)`
- `tcl_lassign(words, text, value)`
- `tcl_dict(words, text, value)`
- `tcl_format(words, text, value)`
- `tcl_scan(words, text, value)`
- `tcl_string(words, text, value)`
- `tcl_regexp(words, text, value)`
- `tcl_regsub(words, text, value)`
- `tclout_expr(words, text)`
- `tcl_tclout(words, text, value)`
- `tcl_tcloutr(words, text, value)`
- `argstr(words)`
- `xs_data(words, text, value)`
- `xs_ignore(words, text, value)`
- `xs_notice(words, text, value)`
- `xs_model(words, text, value)`
- `xs_fit(words, text, value)`
- `xs_error(words, text, value)`
- `xs_statistic(words, text, value)`
- `xs_query(words, text, value)`
- `xs_abund(words, text, value)`
- `xs_xsect(words, text, value)`
- `xs_chatter(words, text, value)`
- `xs_flux(words, text, value)`
- `xs_lumin(words, text, value)`
- `xs_energies(words, text, value)`
- `xs_cpd(words, text, value)`
- `xs_null(words, text, value)`
- `xs_save(words, text, value)`
