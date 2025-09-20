# App Privacy Reset

An Alfred workflow for resetting app privacy permissions on macOS.

## Features

- Reset all privacy permissions for selected applications
- Triggered by hotkey (Cmd+R) or keyword "Reset"
- Search and select apps by name
- Uses macOS `tccutil` to clear permissions

## Usage

1. Activate Alfred
2. Type "Reset" followed by app name, or
3. Use hotkey Cmd+R to trigger directly
4. Select the app whose permissions you want to reset
5. Privacy permissions will be cleared and you'll receive a notification

## Requirements

- Alfred 5 with Powerpack
- macOS 10.14+

## License

MIT License - see [LICENSE](../LICENSE) file