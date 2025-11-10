#!/bin/bash

##############################################################################
# Cybertruck Airflow Calculator - Enhanced Update Script
# This script updates the airflow-calc package to the latest version
##############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="${HOME}/.local/airflow-calc"
VERSION_FILE="${INSTALL_DIR}/.version"
REPO_URL="https://github.com/IceNet-01/Airflow-Calc"
TEMP_DIR="/tmp/airflow-calc-update-$$"
BACKUP_DIR=""
UPDATE_LOG="${INSTALL_DIR}/update.log"

##############################################################################
# Helper Functions
##############################################################################

print_header() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║   CYBERTRUCK AIRFLOW CALCULATOR - AUTO UPDATER          ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
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
    echo ""
    echo -e "${CYAN}${BOLD}▸ $1${NC}"
}

print_feature() {
    echo -e "  ${MAGENTA}⚡${NC} $1"
}

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$UPDATE_LOG"
}

check_installation() {
    print_step "Checking for existing installation..."

    if [ ! -d "$INSTALL_DIR" ]; then
        print_error "Airflow Calculator is not installed."
        print_info "Please run the installer first: ./install.sh"
        log_message "ERROR: No installation found"
        exit 1
    fi

    print_success "Installation found at $INSTALL_DIR"
    log_message "Installation found"
}

get_current_version() {
    print_step "Detecting current version..."

    if [ -f "$VERSION_FILE" ]; then
        CURRENT_VERSION=$(head -n 1 "$VERSION_FILE")
        INSTALL_DATE=$(tail -n 1 "$VERSION_FILE")

        echo -e "  ${BOLD}Current Version:${NC} ${GREEN}$CURRENT_VERSION${NC}"
        echo -e "  ${BOLD}Installed:${NC} $INSTALL_DATE"

        log_message "Current version: $CURRENT_VERSION"
    else
        CURRENT_VERSION="unknown"
        print_warning "Version information not found"
        echo -e "  ${BOLD}Current Version:${NC} ${YELLOW}Unknown${NC}"
        log_message "WARNING: Version file not found"
    fi
}

check_git() {
    if ! command -v git &> /dev/null; then
        print_error "git is not installed"
        print_info "Install git to enable automatic updates:"
        echo "  • Ubuntu/Debian: sudo apt install git"
        echo "  • macOS: brew install git"
        echo "  • Fedora: sudo dnf install git"
        echo ""
        echo -n "Continue with manual reinstallation? [y/N] "
        read -r response
        response=${response:-N}

        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_info "Update cancelled"
            exit 0
        fi
        return 1
    fi
    return 0
}

check_for_updates() {
    print_step "Checking for updates from GitHub..."

    if ! check_git; then
        return 1
    fi

    # Clone repository to temp directory
    print_info "Fetching latest release..."
    rm -rf "$TEMP_DIR"

    if ! git clone --quiet --depth 1 --branch main "$REPO_URL" "$TEMP_DIR" 2>/dev/null; then
        print_error "Failed to fetch updates from GitHub"
        print_info "Check your internet connection and try again"
        echo "  Repository: $REPO_URL"
        log_message "ERROR: Failed to clone repository"
        exit 1
    fi

    cd "$TEMP_DIR"

    # Get latest version
    if [ -f "setup.py" ]; then
        LATEST_VERSION=$(grep "__version__" src/airflow_calc/__init__.py | cut -d'"' -f2 2>/dev/null || \
                        grep "version=" setup.py | cut -d"'" -f2 | head -1)

        echo ""
        echo -e "  ${BOLD}Latest Version:${NC} ${GREEN}$LATEST_VERSION${NC}"
        log_message "Latest version: $LATEST_VERSION"

        # Compare versions
        if [ "$CURRENT_VERSION" == "$LATEST_VERSION" ]; then
            echo ""
            print_success "You already have the latest version!"
            echo ""
            echo -n "Do you want to reinstall anyway? [y/N] "
            read -r response
            response=${response:-N}

            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                print_info "Update cancelled"
                rm -rf "$TEMP_DIR"
                exit 0
            fi
        else
            echo ""
            print_warning "Update available: ${CURRENT_VERSION} → ${LATEST_VERSION}"
            show_whats_new
        fi
    else
        print_error "Cannot determine latest version"
        exit 1
    fi
}

show_whats_new() {
    print_step "What's New in Version $LATEST_VERSION"

    # Check for CHANGELOG or recent commits
    if [ -f "CHANGELOG.md" ]; then
        echo ""
        head -n 20 CHANGELOG.md | while IFS= read -r line; do
            print_feature "$line"
        done
    elif [ -f "FEATURES.md" ]; then
        echo ""
        print_info "New features and improvements available"
        print_feature "Enhanced 3D visualization"
        print_feature "Improved GUI interfaces"
        print_feature "Better performance"
        print_feature "Bug fixes and stability improvements"
    else
        # Show recent commits
        echo ""
        print_info "Recent changes:"
        git log --oneline --max-count=5 2>/dev/null | while IFS= read -r line; do
            print_feature "$line"
        done
    fi

    echo ""
    echo -n "Proceed with update? [Y/n] "
    read -r response
    response=${response:-Y}

    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Update cancelled"
        rm -rf "$TEMP_DIR"
        exit 0
    fi
}

backup_installation() {
    print_step "Creating backup of current installation..."

    BACKUP_DIR="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"

    if cp -r "$INSTALL_DIR" "$BACKUP_DIR" 2>/dev/null; then
        local size=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
        print_success "Backup created: $BACKUP_DIR"
        echo -e "  ${BOLD}Size:${NC} $size"
        log_message "Backup created: $BACKUP_DIR"
    else
        print_error "Failed to create backup"
        echo -n "Continue without backup? [y/N] "
        read -r response
        response=${response:-N}

        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            print_info "Update cancelled"
            exit 1
        fi
    fi
}

perform_update() {
    print_step "Installing update..."

    cd "$TEMP_DIR"

    if [ ! -f "install.sh" ]; then
        print_error "Installation script not found in repository"
        rollback_on_failure
        exit 1
    fi

    # Make installer executable
    chmod +x install.sh

    # Run installation
    print_info "Running installer (this may take a minute)..."
    echo ""

    if bash install.sh; then
        print_success "Installation completed successfully"
        log_message "Update installed successfully"
    else
        print_error "Installation failed"
        rollback_on_failure
        exit 1
    fi
}

rollback_on_failure() {
    if [ -d "$BACKUP_DIR" ]; then
        print_warning "Rolling back to previous version..."

        rm -rf "$INSTALL_DIR"
        mv "$BACKUP_DIR" "$INSTALL_DIR"

        print_success "Rollback completed"
        print_info "Your previous installation has been restored"
        log_message "Rolled back to backup: $BACKUP_DIR"
    else
        print_error "No backup available for rollback"
    fi
}

cleanup() {
    print_step "Cleaning up temporary files..."

    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi

    print_success "Cleanup completed"
    log_message "Cleanup completed"
}

verify_update() {
    print_step "Verifying installation..."

    local errors=0

    # Test CLI
    if command -v airflow-calc &> /dev/null; then
        NEW_VERSION=$(airflow-calc --version 2>&1 | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
        print_success "CLI verified - Version: $NEW_VERSION"
    else
        print_error "CLI command not found"
        errors=$((errors + 1))
    fi

    # Test GUI commands exist
    if [ -x "${HOME}/.local/bin/airflow-calc-gui" ]; then
        print_success "2D GUI command verified"
    else
        print_warning "2D GUI command not found"
        errors=$((errors + 1))
    fi

    if [ -x "${HOME}/.local/bin/airflow-calc-3d" ]; then
        print_success "3D GUI command verified"
    else
        print_warning "3D GUI command not found"
        errors=$((errors + 1))
    fi

    if [ $errors -eq 0 ]; then
        log_message "Verification successful - version: $NEW_VERSION"
    else
        print_warning "$errors issue(s) found"
        print_info "Try restarting your terminal"
        log_message "Verification completed with $errors warnings"
    fi
}

clean_old_backups() {
    print_step "Cleaning old backups..."

    local backup_count=$(find "$(dirname "$INSTALL_DIR")" -maxdepth 1 -name ".local/airflow-calc.backup.*" -type d 2>/dev/null | wc -l)

    if [ "$backup_count" -gt 3 ]; then
        print_info "Found $backup_count old backups"
        echo -n "Keep only the 3 most recent backups? [Y/n] "
        read -r response
        response=${response:-Y}

        if [[ "$response" =~ ^[Yy]$ ]]; then
            # Keep only the 3 most recent backups
            find "$(dirname "$INSTALL_DIR")" -maxdepth 1 -name "airflow-calc.backup.*" -type d | \
                sort -r | tail -n +4 | while read -r dir; do
                rm -rf "$dir"
                print_info "Removed old backup: $(basename "$dir")"
            done
            print_success "Old backups cleaned"
        fi
    fi
}

print_completion_message() {
    echo ""
    echo -e "${GREEN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║          UPDATE COMPLETED SUCCESSFULLY! 🎉              ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${BOLD}Updated Version:${NC} ${GREEN}$NEW_VERSION${NC}"
    echo ""
    echo -e "${BOLD}Test the Update:${NC}"
    echo -e "  ${CYAN}airflow-calc --version${NC}           # Check version"
    echo -e "  ${CYAN}airflow-calc -s 65 --unit mph${NC}    # Test CLI"
    echo -e "  ${CYAN}airflow-calc-gui${NC}                 # Test 2D GUI"
    echo -e "  ${CYAN}airflow-calc-3d${NC}                  # Test 3D GUI (Recommended!)"
    echo ""
    echo -e "${BOLD}Documentation:${NC}"
    echo -e "  ${CYAN}cat ~/.local/airflow-calc/FEATURES.md${NC}  # See all features"
    echo -e "  ${CYAN}cat ~/.local/airflow-calc/README.md${NC}    # Quick reference"
    echo ""
    echo -e "${BOLD}What's New:${NC}"
    echo -e "  Visit: ${CYAN}$REPO_URL${NC}"
    echo ""

    if [ -d "$BACKUP_DIR" ]; then
        echo -e "${BOLD}Backup Location:${NC}"
        echo -e "  $BACKUP_DIR"
        echo -e "  ${YELLOW}(Can be safely deleted if update works correctly)${NC}"
        echo ""
    fi

    log_message "Update completed successfully"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -f, --force         Force update even if already latest"
    echo "  -n, --no-backup     Skip backup creation"
    echo "  --clean-backups     Clean old backups only"
    echo ""
    echo "Examples:"
    echo "  $0                  # Normal update"
    echo "  $0 --force          # Force reinstall"
    echo "  $0 --clean-backups  # Clean old backups"
}

##############################################################################
# Main Update Process
##############################################################################

main() {
    # Parse arguments
    FORCE_UPDATE=false
    NO_BACKUP=false
    CLEAN_ONLY=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -f|--force)
                FORCE_UPDATE=true
                shift
                ;;
            -n|--no-backup)
                NO_BACKUP=true
                shift
                ;;
            --clean-backups)
                CLEAN_ONLY=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    print_header

    # Log start
    log_message "========== Update started =========="

    if [ "$CLEAN_ONLY" = true ]; then
        check_installation
        clean_old_backups
        exit 0
    fi

    # Run update process
    check_installation
    get_current_version
    check_for_updates

    if [ "$NO_BACKUP" = false ]; then
        backup_installation
    fi

    perform_update
    cleanup
    verify_update
    clean_old_backups
    print_completion_message

    log_message "========== Update finished =========="
}

# Trap errors and cleanup
trap 'print_error "Update interrupted"; cleanup; exit 1' INT TERM

# Run main update
main "$@"
