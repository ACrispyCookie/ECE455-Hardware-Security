CC      := gcc
CFLAGS  := -O2
LDFLAGS :=

# Programs to build
TARGETS := pagefaulter ramear

# Per-target flags
pagefaulter_CFLAGS := -pthread
ramear_CFLAGS     := -msse2 -Wall -std=c99

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  all         Build all programs ($(TARGETS))"
	@echo "  pagefaulter  Build pagefaulter"
	@echo "  ramear      Build ramear"
	@echo "  clean       Remove built binaries"
	@echo "  help        Show this help message"

all: $(TARGETS)

pagefaulter: pagefaulter.c
	$(CC) $(CFLAGS) $(pagefaulter_CFLAGS) $< -o $@

ramear: ramear.c
	$(CC) $(CFLAGS) $(ramear_CFLAGS) $< -o $@

clean:
	rm -f $(TARGETS)

.PHONY: all clean
