#!/bin/bash

##############################################################################
# Cybertruck Airflow Calculator - Installation Script
# This script installs the airflow-calc package and its dependencies
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="${HOME}/.local/airflow-calc"
BIN_DIR="${HOME}/.local/bin"
VERSION_FILE="${INSTALL_DIR}/.version"

##############################################################################
# Helper Functions
##############################################################################

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "============================================================"
    echo "  CYBERTRUCK AIRFLOW CALCULATOR - INSTALLER"
    echo "============================================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ Error: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}! Warning: $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_step() {
    echo -e "${CYAN}${BOLD}▸ $1${NC}"
}

check_python() {
    print_step "Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python 3 is not installed. Please install Python 3.7 or higher."
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_error "Python 3.7 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION found"
}

check_pip() {
    print_step "Checking pip installation..."

    if $PYTHON_CMD -m pip --version &> /dev/null; then
        print_success "pip is available"
    else
        print_error "pip is not available. Please install pip."
        exit 1
    fi
}

check_existing_installation() {
    print_step "Checking for existing installation..."

    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Existing installation found at $INSTALL_DIR"
        echo -n "Do you want to upgrade the existing installation? [Y/n] "
        read -r response
        response=${response:-Y}

        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled."
            exit 0
        fi

        print_info "Removing existing installation..."
        rm -rf "$INSTALL_DIR"
    fi
}

create_directories() {
    print_step "Creating installation directories..."

    mkdir -p "$INSTALL_DIR"
    mkdir -p "$BIN_DIR"

    print_success "Directories created"
}

install_package() {
    print_step "Installing Airflow Calculator..."

    # Copy source files
    cp -r src "$INSTALL_DIR/"
    cp setup.py "$INSTALL_DIR/"
    cp requirements.txt "$INSTALL_DIR/"
    cp LICENSE "$INSTALL_DIR/" 2>/dev/null || true

    # Copy documentation
    cp -r docs "$INSTALL_DIR/" 2>/dev/null || true
    cp -r examples "$INSTALL_DIR/" 2>/dev/null || true
    cp README.md "$INSTALL_DIR/" 2>/dev/null || true
    cp FEATURES.md "$INSTALL_DIR/" 2>/dev/null || true

    cd "$INSTALL_DIR"

    # Create virtual environment
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv venv

    # Activate virtual environment
    source venv/bin/activate

    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip --quiet

    # Install dependencies
    print_info "Installing dependencies..."
    pip install -r requirements.txt --quiet

    # Install package
    print_info "Installing airflow-calc package..."
    pip install -e . --quiet

    print_success "Package installed successfully"
}

create_wrapper_script() {
    print_step "Creating wrapper scripts..."

    # CLI wrapper
    cat > "$BIN_DIR/airflow-calc" << 'EOF'
#!/bin/bash
# Wrapper script for Cybertruck Airflow Calculator CLI

INSTALL_DIR="${HOME}/.local/airflow-calc"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: Airflow Calculator is not installed."
    echo "Please run the installer first."
    exit 1
fi

source "$INSTALL_DIR/venv/bin/activate"
python -m airflow_calc.cli "$@"
EOF

    chmod +x "$BIN_DIR/airflow-calc"

    # 2D GUI wrapper
    cat > "$BIN_DIR/airflow-calc-gui" << 'EOF'
#!/bin/bash
# Wrapper script for Cybertruck Airflow Calculator 2D GUI

INSTALL_DIR="${HOME}/.local/airflow-calc"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: Airflow Calculator is not installed."
    echo "Please run the installer first."
    exit 1
fi

source "$INSTALL_DIR/venv/bin/activate"
python -m airflow_calc.gui "$@"
EOF

    chmod +x "$BIN_DIR/airflow-calc-gui"

    # 3D GUI wrapper
    cat > "$BIN_DIR/airflow-calc-3d" << 'EOF'
#!/bin/bash
# Wrapper script for Cybertruck Airflow Calculator 3D GUI

INSTALL_DIR="${HOME}/.local/airflow-calc"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: Airflow Calculator is not installed."
    echo "Please run the installer first."
    exit 1
fi

source "$INSTALL_DIR/venv/bin/activate"
python -m airflow_calc.gui_3d "$@"
EOF

    chmod +x "$BIN_DIR/airflow-calc-3d"

    print_success "Wrapper scripts created (CLI, 2D GUI, 3D GUI)"
}

update_path() {
    print_step "Checking PATH configuration..."

    # Check if BIN_DIR is in PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        print_warning "$BIN_DIR is not in your PATH"

        # Detect shell
        SHELL_NAME=$(basename "$SHELL")
        case "$SHELL_NAME" in
            bash)
                SHELL_RC="$HOME/.bashrc"
                ;;
            zsh)
                SHELL_RC="$HOME/.zshrc"
                ;;
            fish)
                SHELL_RC="$HOME/.config/fish/config.fish"
                ;;
            *)
                SHELL_RC="$HOME/.profile"
                ;;
        esac

        print_info "Adding $BIN_DIR to PATH in $SHELL_RC"

        # Add to shell RC file
        echo "" >> "$SHELL_RC"
        echo "# Added by Airflow Calculator installer" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"

        print_success "PATH updated in $SHELL_RC"
        print_warning "Please restart your terminal or run: source $SHELL_RC"
    else
        print_success "PATH is already configured"
    fi
}

save_version() {
    print_step "Saving version information..."

    # Extract version from setup.py
    VERSION=$(grep "version=" setup.py | cut -d"'" -f2 | head -1)
    echo "$VERSION" > "$VERSION_FILE"
    echo "$(date +%Y-%m-%d)" >> "$VERSION_FILE"

    print_success "Version $VERSION saved"
}

run_verification() {
    print_step "Verifying installation..."

    # Test CLI
    if "$BIN_DIR/airflow-calc" --version &> /dev/null; then
        print_success "CLI verified"
    else
        print_error "CLI verification failed"
        exit 1
    fi

    # Check GUI wrappers exist
    if [ -x "$BIN_DIR/airflow-calc-gui" ] && [ -x "$BIN_DIR/airflow-calc-3d" ]; then
        print_success "GUI wrappers verified"
    else
        print_error "GUI wrapper verification failed"
        exit 1
    fi

    print_success "Installation verified successfully"
}

print_completion_message() {
    echo ""
    echo -e "${GREEN}${BOLD}"
    echo "============================================================"
    echo "  INSTALLATION COMPLETED SUCCESSFULLY!"
    echo "============================================================"
    echo -e "${NC}"
    echo ""
    echo -e "${BOLD}Quick Start - Command Line:${NC}"
    echo -e "  ${CYAN}airflow-calc -s 65 --unit mph${NC}       # Analyze at 65 mph"
    echo -e "  ${CYAN}airflow-calc --range 0 120 --unit kmh${NC} # Speed range analysis"
    echo -e "  ${CYAN}airflow-calc --show-specs${NC}          # Show Cybertruck specs"
    echo -e "  ${CYAN}airflow-calc --help${NC}                # Show all options"
    echo ""
    echo -e "${BOLD}Quick Start - Graphical Interfaces:${NC}"
    echo -e "  ${CYAN}airflow-calc-gui${NC}                   # Launch 2D GUI"
    echo -e "  ${CYAN}airflow-calc-3d${NC}                    # Launch 3D GUI (Recommended!)"
    echo ""
    echo -e "${BOLD}Documentation:${NC}"
    echo -e "  ${CYAN}cat docs/USER_GUIDE.md${NC}            # Full user guide"
    echo -e "  ${CYAN}cat FEATURES.md${NC}                   # Complete feature list"
    echo ""
    echo -e "${BOLD}Installation location:${NC}"
    echo -e "  $INSTALL_DIR"
    echo ""

    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo -e "${YELLOW}${BOLD}IMPORTANT:${NC} Please restart your terminal or run:"
        echo -e "  ${CYAN}source ~/.bashrc${NC}  (or ~/.zshrc for zsh)"
        echo ""
    fi
}

##############################################################################
# Main Installation
##############################################################################

main() {
    print_header

    # Check if running in the correct directory
    if [ ! -f "setup.py" ]; then
        print_error "Please run this script from the Airflow-Calc directory"
        exit 1
    fi

    # Run installation steps
    check_python
    check_pip
    check_existing_installation
    create_directories
    install_package
    create_wrapper_script
    update_path
    save_version
    run_verification
    print_completion_message
}

# Run main installation
main
