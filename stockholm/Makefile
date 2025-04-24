# === CONFIG ===
SRC         := stockholm.sh
NAME        := stockholm
LOG_DIR     := $(HOME)/infection
BIN         := $(NAME)
SHC_DIR     := $(CURDIR)/shc
SHC         := $(SHC_DIR)/src/shc
OPENSSL     := openssl

# === COLORS ===
GREEN       := \033[1;32m
RED         := \033[1;31m
RESET       := \033[0m

# === DEFAULT TARGET ===
all: compile_shc bin

# === COMPILE 'shc' BINARY ===
compile_shc:
	@if [ ! -f $(SHC) ]; then \
		echo "$(GREEN)[+] Compiling shc...$(RESET)"; \
		cd $(SHC_DIR) && ./configure && make; \
	else \
		echo "$(GREEN)[✓] 'shc' is already compiled. $(RESET)"; \
	fi

# === COMPILE TO BINARY ===
bin: check_tools $(SRC)
	@echo "$(GREEN)[+] Compiling $(SRC) into binary '$(BIN)'...$(RESET)"
	@$(SHC) -f $(SRC) -o $(BIN)
	@chmod +x $(BIN)
	@echo "$(GREEN)[✓] Done. Run it with ./$(BIN)$(RESET)"

# === CHECK FOR DEPENDENCIES ===
check_tools:
	@command -v $(OPENSSL) >/dev/null || { echo "$(RED)[!] 'openssl' not found. Install it: sudo apt install openssl$(RESET)"; exit 1; }
# === CLEAN GENERATED FILES ===
clean:
	   @rm -f $(SRC).x.c $(SRC).x
	@echo "$(GREEN)[✓] Cleaned build artifacts$(RESET)"

# === FULL CLEAN ===
fclean: clean
		@rm -f $(BIN)
	@rm -f $(LOG_DIR)/$(SRC)
	@echo "$(GREEN)[✓] Removed binary and copied source$(RESET)"

# === PHONY TARGETS ===
.PHONY: all setup compile_shc bin clean fclean check_tools
