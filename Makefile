.PHONY: test fmt check all

# --clean keeps the user's own config off the runtimepath; without it a stowed
# or otherwise installed copy of this plugin shadows the working tree and the
# tests silently exercise the wrong files.
NVIM ?= nvim
RTP := $(CURDIR)

all: check test

test:
	$(NVIM) --headless --clean --cmd 'set rtp^=$(RTP)' -l tests/smoke.lua

check:
	stylua --check .

fmt:
	stylua .
