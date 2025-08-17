# Increasing Initial Deck Capacity

1. Start a New Game in mGBA.
2. Search 16-bit value = current deck capacity.
3. Add a **Write** watchpoint in the Debugger on that RAM address.
4. Restart game → breakpoint hits during initialization.
5. Look at disassembly:
   - `MOV rX, #imm` → immediate constant in code
   - `LDR rX, =literal` → check literal pool (ROM offset)
   - `LDR rX, [rZ]` → value loaded from default save block

6. Once ROM file offset is known:
   - Use `scripts/patch_halfword.py` (16-bit)
   - Or `scripts/patch_word.py` (32-bit)

7. Save patched ROM into `rom-hacked/`, start a fresh New Game to verify.

