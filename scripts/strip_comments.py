\
import os
import sys
import io
import tokenize
from typing import List, Tuple
\
EXCLUDES = {'.git', '.venv', 'node_modules', 'dist', 'build', '.next', '.cache'}
PY_EXTS = {'.py'}
JS_EXTS = {'.js', '.jsx'}
CSS_EXTS = {'.css'}
HTML_EXTS = {'.html', '.htm'}
\
\
def should_skip_dir(dirname: str) -> bool:
    return dirname in EXCLUDES or dirname.startswith('.') and dirname not in {'.', '..'}
def strip_python_comments(code: str) -> str:
    """Remove Python comments while preserving docstrings and code formatting."""
    try:
        buf = io.StringIO(code)
        tokens = list(tokenize.generate_tokens(buf.readline))
    except Exception:
        return code                                        
    out_tokens: List[tokenize.TokenInfo] = []
    prev_end: Tuple[int, int] = (1, 0)
    \
    for tok in tokens:
        tok_type = tok.type
        tok_str = tok.string
        if tok_type == tokenize.COMMENT:
            \
            continue
        if tok_type == tokenize.NL and (not out_tokens or out_tokens[-1].type in (tokenize.NEWLINE, tokenize.NL)):
            \
            continue
        out_tokens.append(tok)
    try:
        out = tokenize.untokenize(out_tokens)
        return out
    except Exception:
        return code
def strip_js_like_comments(code: str) -> str:
    """
    Remove // and /* */ comments from JS/JSX while respecting strings and template literals.
    Does not attempt to parse regex literals beyond ensuring we're not inside strings.
    """
    i = 0
    n = len(code)
    out_chars = []
    in_single = False
    in_double = False
    in_backtick = False
    in_line_comment = False
    in_block_comment = False
    backtick_braces = 0                                          
    \
    def prev_char() -> str:
        return out_chars[-1] if out_chars else ''
    while i < n:
        ch = code[i]
        ch2 = code[i:i+2]
        \
        if in_line_comment:
            if ch == '\n':
                in_line_comment = False
                out_chars.append(ch)
            i += 1
            continue
        if in_block_comment:
            if ch2 == '*/':
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue
        if in_single:
            out_chars.append(ch)
            if ch == '\\':
                \
                if i + 1 < n:
                    out_chars.append(code[i+1])
                    i += 2
                    continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            out_chars.append(ch)
            if ch == '\\':
                if i + 1 < n:
                    out_chars.append(code[i+1])
                    i += 2
                    continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if in_backtick:
            out_chars.append(ch)
            if ch == '\\':
                if i + 1 < n:
                    out_chars.append(code[i+1])
                    i += 2
                    continue
            if ch == '{' and prev_char() == '$':
                backtick_braces += 1
            elif ch == '}' and backtick_braces > 0:
                backtick_braces -= 1
            elif ch == '`' and backtick_braces == 0:
                in_backtick = False
            i += 1
            continue
        if ch2 == '//':
            in_line_comment = True
            i += 2
            continue
        if ch2 == '/*':
            in_block_comment = True
            i += 2
            continue
        if ch == "'":
            in_single = True
            out_chars.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = True
            out_chars.append(ch)
            i += 1
            continue
        if ch == '`':
            in_backtick = True
            out_chars.append(ch)
            i += 1
            continue
        out_chars.append(ch)
        i += 1
    return ''.join(out_chars)
def strip_css_comments(code: str) -> str:
    \
    i = 0
    n = len(code)
    out_chars = []
    in_single = False
    in_double = False
    in_block_comment = False
    \
    while i < n:
        ch = code[i]
        ch2 = code[i:i+2]
        if in_block_comment:
            if ch2 == '*/':
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue
        if in_single:
            out_chars.append(ch)
            if ch == '\\':
                if i + 1 < n:
                    out_chars.append(code[i+1])
                    i += 2
                    continue
            if ch == "'":
                in_single = False
            i += 1
            continue
        if in_double:
            out_chars.append(ch)
            if ch == '\\':
                if i + 1 < n:
                    out_chars.append(code[i+1])
                    i += 2
                    continue
            if ch == '"':
                in_double = False
            i += 1
            continue
        if ch2 == '/*':
            in_block_comment = True
            i += 2
            continue
        if ch == "'":
            in_single = True
            out_chars.append(ch)
            i += 1
            continue
        if ch == '"':
            in_double = True
            out_chars.append(ch)
            i += 1
            continue
        out_chars.append(ch)
        i += 1
    return ''.join(out_chars)
def strip_html_comments(code: str) -> str:
    out = []
    i = 0
    n = len(code)
    while i < n:
        if code.startswith('<!--', i):
            j = code.find('-->', i + 4)
            if j == -1:
                \
                break
            i = j + 3
        else:
            out.append(code[i])
            i += 1
    return ''.join(out)
def process_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False
    original = content
    if ext in PY_EXTS:
        content = strip_python_comments(content)
    elif ext in JS_EXTS:
        content = strip_js_like_comments(content)
    elif ext in CSS_EXTS:
        content = strip_css_comments(content)
    elif ext in HTML_EXTS:
        content = strip_html_comments(content)
    else:
        return False
    if content != original:
        try:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            return True
        except Exception:
            return False
    return False
def walk_and_process(root: str) -> Tuple[int, int]:
    changed = 0
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        \
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in PY_EXTS | JS_EXTS | CSS_EXTS | HTML_EXTS:
                total += 1
                fullp = os.path.join(dirpath, fname)
                if process_file(fullp):
                    changed += 1
    return changed, total
def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print('Usage: strip_comments.py <path1> [<path2> ...]')
        return 2
    total_changed = 0
    total_files = 0
    for p in argv[1:]:
        if os.path.isdir(p):
            ch, tot = walk_and_process(p)
            print(f"Processed {p}: changed {ch}/{tot} files")
            total_changed += ch
            total_files += tot
        elif os.path.isfile(p):
            if process_file(p):
                print(f"Changed {p}")
                total_changed += 1
            total_files += 1
    print(f"Done: changed {total_changed}/{total_files} files")
    return 0
if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
