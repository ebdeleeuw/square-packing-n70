# 70-square rational certificate

70 unit squares fit in a square of exact side **8.88096037156625096037155737**.
This is a precision refinement of [Ryan Xu's construction](https://github.com/ry-xu/square_packing/tree/8dc415296f697f5140caea27c7a0193d52deb4e6), smaller than his published rational certificate by exactly `0.00000000014263000000014263`.

Run with Python 3, standard library only:

```sh
python verify_exact.py certificate.json --check
```

The exact rational checker verifies 70 unit squares, containment, and all 2,415 pairs without an overlap tolerance. The certificate stores rational centers in a centered box and rational `t = tan(theta/2)`; rotation axes are derived exactly. See `verification.json` for local results, timings, and hashes.

`external-positive.txt` is a 60-digit export accepted by [David Ellsworth's checker](https://github.com/Davidebyzero/packing_squares_in_squares__tools/blob/79f8a378d52e757d70f7cfb2c2f7a24a53da0204/check_packing.py): `python check_packing.py external-positive.txt 40`. Its output is included.

Original arrangement credit: Ryan Xu. Refinement and rational certification: ebdeleeuw, with OpenAI Codex assistance. The in-project generator and exact checker were developed together; the external checker is independently authored software run locally. No new arrangement family, local/global optimality proof, proof-assistant formalization, or external human review is claimed. Catalogue registration is pending submission and review.
