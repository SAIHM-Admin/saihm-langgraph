# Third-party notices

`saihm-langgraph` is Apache-2.0. It redistributes a small amount of third-party code, listed
here with its own license.

## LangGraph (langgraph-checkpoint)

`src/saihm_memory/_lg_filter.py` contains verbatim copies of three private helpers from
`langgraph/store/memory/__init__.py` (langgraph-checkpoint 4.2.0): `_compare_values`,
`_does_match`, and `_apply_operator`, renamed with a `_vendored_` prefix but otherwise unmodified.

They are used only as a fallback: the module imports LangGraph's own helpers when they are
importable and falls back to these copies when they are not, so `SaihmStore` keeps filter and
namespace semantics identical to LangGraph's reference `InMemoryStore` either way.

Source: https://github.com/langchain-ai/langgraph

```
MIT License

Copyright (c) 2024 LangChain, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
