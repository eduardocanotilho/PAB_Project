REPORT="diff_report.txt"
: > "$REPORT"   # empty/create the report file

pass=0
fail=0

for expected in tests/output*.txt; do
    x="${expected#tests/output}"
    x="${x%.txt}"
    ours="our_tests/${x}.txt"

    if [ ! -f "$ours" ]; then
        echo "MISSING: $ours" | tee -a "$REPORT"
        fail=$((fail + 1))
        continue
    fi

    if diff -u --label "expected (tests/output${x}.txt)" --label "ours ($ours)" \
            "$expected" "$ours" > /tmp/diff_tmp.txt; then
        echo "PASS: $x"
        pass=$((pass + 1))
    else
        echo "FAIL: $x"
        {
            echo "===== Test $x ====="
            cat /tmp/diff_tmp.txt
            echo
        } >> "$REPORT"
        fail=$((fail + 1))
    fi
done

rm -f /tmp/diff_tmp.txt

echo
echo "Passed: $pass | Failed: $fail"
echo "Differences saved to $REPORT"
