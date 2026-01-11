CC      := gcc
CFLAGS  := -O2
LDFLAGS :=

# Programs to build
TARGETS := segfaulter ramear

# Per-target flags
segfaulter_CFLAGS := -pthread
ramear_CFLAGS     := -msse2 -Wall -std=c99

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  all         Build all programs ($(TARGETS))"
	@echo "  segfaulter  Build segfaulter"
	@echo "  ramear      Build ramear"
	@echo "  clean       Remove built binaries"
	@echo "  help        Show this help message"

all: $(TARGETS)

segfaulter: segfaulter.c
	$(CC) $(CFLAGS) $(segfaulter_CFLAGS) $< -o $@

ramear: ramear.c
	$(CC) $(CFLAGS) $(ramear_CFLAGS) $< -o $@

clean:
	rm -f $(TARGETS)

.PHONY: all clean
