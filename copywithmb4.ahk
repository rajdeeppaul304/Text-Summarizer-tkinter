; AutoHotkey script to copy selected text with Mouse Button 4 (MB4)

; Set up the hotkey for Mouse Button 4 (XButton1)
XButton1::
{
    ; Send Ctrl+C to copy the selected text
    Send, ^c
    ; Wait a moment to ensure the clipboard has been updated
    ClipWait, 1
    ; If the clipboard is empty, show a message
    if (ErrorLevel) {
        ToolTip, Failed to copy text.
        Sleep, 2000
        ToolTip
    } else {
        ; Show the copied text in a tooltip
        ToolTip, %clipboard%
        Sleep, 2000
        ToolTip
    }
    return
}

