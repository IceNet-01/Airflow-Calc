#!/bin/bash

##############################################################################
# Cybertruck Airflow Calculator - Update Script
# This script updates the airflow-calc package to the latest version
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
VERSION_FILE="${INSTALL_DIR}/.version"
REPO_URL="https://github.com/IceNet-01/Airflow-Calc"
TEMP_DIR="/tmp/airflow-calc-update"

##############################################################################
# Helper Functions
##############################################################################

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "============================================================"
    echo "  CYBERTRUCK AIRFLOW CALCULATOR - UPDATER"
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
    print_step "Checking for existing installation..."

    if [ ! -d "$INSTALL_DIR" ]; then
        print_error "Airflow Calculator is not installed."
        print_info "Please run the installer first: ./install.sh"
        exit 1
    fi

    print_success "Installation found"
}

get_current_version() {
    if [ -f "$VERSION_FILE" ]; then
        CURRENT_VERSION=$(head -n 1 "$VERSION_FILE")
        INSTALL_DATE=$(tail -n 1 "$VERSION_FILE")
        print_info "Current version: $CURRENT_VERSION (installed: $INSTALL_DATE)"
    else
        CURRENT_VERSION="unknown"
        print_warning "Version information not found"
    fi
}

check_for_updates() {
    print_step "Checking for updates..."

    # Check if git is available
    if ! command -v git &> /dev/null; then
        print_warning "git is not installed. Cannot check for updates automatically."
        echo -n "Do you want to proceed with reinstallation anyway? [Y/n] "
        read -r response
        response=${response:-Y}

        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_info "Update cancelled."
            exit 0
        fi
        return
    fi

    # Clone repository to temp directory
    print_info "Fetching latest version..."
    rm -rf "$TEMP_DIR"

    if git clone --quiet --depth 1 "$REPO_URL" "$TEMP_DIR" 2>/dev/null; then
        cd "$TEMP_DIR"

        # Get latest version from setup.py
        if [ -f "setup.py" ]; then
            LATEST_VERSION=$(grep "version=" setup.py | cut -d"'" -f2 | head -1)
            print_info "Latest version: $LATEST_VERSION"

            if [ "$CURRENT_VERSION" == "$LATEST_VERSION" ]; then
                print_success "You already have the latest version!"
                echo -n "Do you want to reinstall anyway? [y/N] "
                read -r response
                response=${response:-N}

                if [[ ! "$response" =~ ^[Yy]$ ]]; then
                    print_info "Update cancelled."
                    rm -rf "$TEMP_DIR"
                    exit 0
                fi
            else
                print_warning "Update available: $CURRENT_VERSION → $LATEST_VERSION"
            fi
        fi
    else
        print_error "Failed to fetch updates from repository"
        print_info "Please check your internet connection and try again"
        exit 1
    fi
}

backup_installation() {
    print_step "Creating backup of current installation..."

    BACKUP_DIR="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
    cp -r "$INSTALL_DIR" "$BACKUP_DIR"

    print_success "Backup created at: $BACKUP_DIR"
    print_info "If update fails, you can restore from backup"
}

perform_update() {
    print_step "Updating Airflow Calculator..."

    # Use the cloned repository
    cd "$TEMP_DIR"

    # Run the installation script
    if [ -f "install.sh" ]; then
        print_info "Running installation script..."
        bash install.sh
    else
        print_error "Installation script not found in repository"
        exit 1
    fi
}

cleanup() {
    print_step "Cleaning up temporary files..."

    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi

    print_success "Cleanup completed"
}

verify_update() {
    print_step "Verifying update..."

    if command -v airflow-calc &> /dev/null; then
        NEW_VERSION=$(airflow-calc --version 2>&1 | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
        print_success "Update verified - Version: $NEW_VERSION"
    else
        print_error "Verification failed - command not found"
        print_warning "You may need to restart your terminal"
    fi
}

print_completion_message() {
    echo ""
    echo -e "${GREEN}${BOLD}"
    echo "============================================================"
    echo "  UPDATE COMPLETED SUCCESSFULLY!"
    echo "============================================================"
    echo -e "${NC}"
    echo ""
    echo -e "${BOLD}What's New:${NC}"
    echo -e "  Check the changelog at: ${CYAN}$REPO_URL${NC}"
    echo ""
    echo -e "${BOLD}Test the update:${NC}"
    echo -e "  ${CYAN}airflow-calc --version${NC}"
    echo -e "  ${CYAN}airflow-calc -s 65 --unit mph${NC}"
    echo ""
}

##############################################################################
# Main Update Process
##############################################################################

main() {
    print_header

    check_installation
    get_current_version
    check_for_updates
    backup_installation
    perform_update
    cleanup
    verify_update
    print_completion_message
}

# Run main update
main
