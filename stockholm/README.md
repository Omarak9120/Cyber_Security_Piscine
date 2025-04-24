
# Stockholm

**Stockholm** is a ransomware simulation tool that encrypts files with AES-256 encryption. It also supports decryption. It uses `openssl` for encryption and decryption.

## Requirements

- **openssl**
- **bash**

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd stockholm
    ```

2. Compile `shc`:
    ```bash
    make compile_shc
    ```

3. Build the binary:
    ```bash
    make bin
    ```

## Usage

### Basic Commands

- **Encrypt files**:
    ```bash
    ./stockholm
    ```

- **Decrypt files**:
    ```bash
    ./stockholm -r
    ```

### Options

- `-h`, `--help`: Show help message
- `-v`, `--version`: Show version
- `-r`, `--reverse`: Decrypt files
- `-s`, `--silent`: Silent mode
