#!/bin/bash

##############################################################################
# Cybertruck Airflow Calculator - Uninstaller Script
# This script removes the airflow-calc package and cleans up all files
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
WRAPPER_SCRIPT="${BIN_DIR}/airflow-calc"

##############################################################################
# Helper Functions
##############################################################################

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "============================================================"
    echo "  CYBERTRUCK AIRFLOW CALCULATOR - UNINSTALLER"
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

check_installation() {
    print_step "Checking for installation..."

    if [ ! -d "$INSTALL_DIR" ]; then
        print_warning "Airflow Calculator is not installed at $INSTALL_DIR"

        # Check if wrapper script exists
        if [ -f "$WRAPPER_SCRIPT" ]; then
            print_info "Found orphaned wrapper script"
            return 0
        else
            print_info "Nothing to uninstall"
            exit 0
        fi
    fi

    print_success "Installation found"
}

confirm_uninstall() {
    echo ""
    echo -e "${YELLOW}${BOLD}WARNING:${NC} This will remove the following:"
    echo "  • Installation directory: $INSTALL_DIR"
    echo "  • Wrapper script: $WRAPPER_SCRIPT"
    echo "  • All configuration and data files"
    echo ""
    echo -n "Are you sure you want to uninstall Airflow Calculator? [y/N] "
    read -r response
    response=${response:-N}

    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled."
        exit 0
    fi
}

remove_installation_directory() {
    print_step "Removing installation directory..."

    if [ -d "$INSTALL_DIR" ]; then
        # Get size before removal
        SIZE=$(du -sh "$INSTALL_DIR" 2>/dev/null | cut -f1)
        print_info "Removing $SIZE of files..."

        rm -rf "$INSTALL_DIR"
        print_success "Installation directory removed"
    else
        print_info "Installation directory not found (already removed)"
    fi
}

remove_wrapper_script() {
    print_step "Removing wrapper scripts..."

    local removed_count=0

    # Remove CLI wrapper
    if [ -f "$WRAPPER_SCRIPT" ]; then
        rm -f "$WRAPPER_SCRIPT"
        removed_count=$((removed_count + 1))
    fi

    # Remove 2D GUI wrapper
    if [ -f "${BIN_DIR}/airflow-calc-gui" ]; then
        rm -f "${BIN_DIR}/airflow-calc-gui"
        removed_count=$((removed_count + 1))
    fi

    # Remove 3D GUI wrapper
    if [ -f "${BIN_DIR}/airflow-calc-3d" ]; then
        rm -f "${BIN_DIR}/airflow-calc-3d"
        removed_count=$((removed_count + 1))
    fi

    if [ $removed_count -gt 0 ]; then
        print_success "Removed $removed_count wrapper script(s)"
    else
        print_info "No wrapper scripts found (already removed)"
    fi
}

clean_backup_files() {
    print_step "Cleaning backup files..."

    # Look for backup directories
    BACKUP_COUNT=0
    for backup in "${INSTALL_DIR}".backup.*; do
        if [ -d "$backup" ]; then
            BACKUP_COUNT=$((BACKUP_COUNT + 1))
        fi
    done

    if [ $BACKUP_COUNT -gt 0 ]; then
        echo -n "Found $BACKUP_COUNT backup(s). Do you want to remove them too? [y/N] "
        read -r response
        response=${response:-N}

        if [[ "$response" =~ ^[Yy]$ ]]; then
            for backup in "${INSTALL_DIR}".backup.*; do
                if [ -d "$backup" ]; then
                    rm -rf "$backup"
                    print_success "Removed backup: $(basename "$backup")"
                fi
            done
        else
            print_info "Keeping backup files"
        fi
    else
        print_info "No backup files found"
    fi
}

clean_shell_config() {
    print_step "Checking shell configuration files..."

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

    if [ -f "$SHELL_RC" ]; then
        # Check if our PATH modification is present
        if grep -q "Added by Airflow Calculator installer" "$SHELL_RC"; then
            print_warning "Found PATH modification in $SHELL_RC"
            echo -n "Do you want to remove it? [y/N] "
            read -r response
            response=${response:-N}

            if [[ "$response" =~ ^[Yy]$ ]]; then
                # Remove our PATH modification
                sed -i.bak '/Added by Airflow Calculator installer/,+1d' "$SHELL_RC"
                print_success "Removed PATH modification from $SHELL_RC"
                print_info "Backup saved as ${SHELL_RC}.bak"
            else
                print_info "Keeping PATH modification (it won't cause issues)"
            fi
        else
            print_info "No PATH modifications found in $SHELL_RC"
        fi
    fi
}

verify_uninstall() {
    print_step "Verifying uninstallation..."

    ISSUES=0

    if [ -d "$INSTALL_DIR" ]; then
        print_error "Installation directory still exists"
        ISSUES=$((ISSUES + 1))
    fi

    # Check all wrapper scripts
    if [ -f "$WRAPPER_SCRIPT" ]; then
        print_error "CLI wrapper script still exists"
        ISSUES=$((ISSUES + 1))
    fi

    if [ -f "${BIN_DIR}/airflow-calc-gui" ]; then
        print_error "2D GUI wrapper script still exists"
        ISSUES=$((ISSUES + 1))
    fi

    if [ -f "${BIN_DIR}/airflow-calc-3d" ]; then
        print_error "3D GUI wrapper script still exists"
        ISSUES=$((ISSUES + 1))
    fi

    # Check if commands are still available
    if command -v airflow-calc &> /dev/null; then
        print_warning "airflow-calc command still available (may be in another location)"
    fi

    if command -v airflow-calc-gui &> /dev/null; then
        print_warning "airflow-calc-gui command still available (may be in another location)"
    fi

    if command -v airflow-calc-3d &> /dev/null; then
        print_warning "airflow-calc-3d command still available (may be in another location)"
    fi

    if [ $ISSUES -eq 0 ]; then
        print_success "Uninstallation verified"
        return 0
    else
        print_error "Uninstallation incomplete ($ISSUES issue(s) found)"
        return 1
    fi
}

print_completion_message() {
    echo ""
    echo -e "${GREEN}${BOLD}"
    echo "============================================================"
    echo "  UNINSTALLATION COMPLETED SUCCESSFULLY!"
    echo "============================================================"
    echo -e "${NC}"
    echo ""
    echo -e "${BOLD}Airflow Calculator has been removed from your system.${NC}"
    echo ""
    echo -e "${BLUE}Thank you for using Cybertruck Airflow Calculator!${NC}"
    echo ""
    echo -e "If you want to reinstall in the future, visit:"
    echo -e "  ${CYAN}https://github.com/IceNet-01/Airflow-Calc${NC}"
    echo ""
}

##############################################################################
# Main Uninstallation Process
##############################################################################

main() {
    print_header

    check_installation
    confirm_uninstall
    remove_installation_directory
    remove_wrapper_script
    clean_backup_files
    clean_shell_config

    if verify_uninstall; then
        print_completion_message
    else
        echo ""
        print_warning "Uninstallation completed with warnings"
        print_info "You may need to manually remove remaining files"
    fi
}

# Run main uninstallation
main
