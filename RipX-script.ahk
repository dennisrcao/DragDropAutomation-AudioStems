; Path to the folder
folderPath := "Z:\\SongsFromMac"

; Open File Explorer at the folder location
Run, explorer.exe %folderPath%

; Wait for File Explorer to open
WinWaitActive, ahk_class CabinetWClass

; Select the first file in the folder
Send, {Down}

; Right-click on the selected file
Send, {AppsKey}

; Wait for the context menu to open
Sleep, 300

; Navigate to "Open with"
Send, w

; Wait for the "Open with" submenu to open
Sleep, 500

; Send down key a few times to ensure it highlights RipX DAW
Loop, 7
{
    Send, {Down}
    Sleep, 200
}

; Press right arrow to open the submenu
Send, {Right}
Sleep, 200

; Select the second item in the right column, open up RipX DAW
Send, {Down}
Sleep, 200
Send, {Enter}

; Wait a moment to ensure the file is being opened with RipX DAW
Sleep, 10000

; Close File Explorer
Send {Alt down}{Tab 1}{Alt up}
Sleep, 200
Send, ^w
Sleep, 200

; Reactivate RipX DAW
Send {Alt down}{Tab 1}{Alt up}

; Press Tab to get to "Rip" button
Sleep, 100
Send, {Tab 1}
Sleep, 100
Send, {Tab 1}
Sleep, 100
Send, {Tab 1}
Sleep, 100

; Type "Enter" button
Send, {Enter}

; Wait 20 minutes
Sleep, 1200000

;Sleep, 100
;Send, {Tab 1}
;Sleep, 100
;Send, {Tab 1}
;Sleep, 100
;Send, {Tab 1}
;Sleep, 100
;Send, {Tab 1}

; Delete any files remaining in the input folder
Loop, Files, %folderPath%\*.*, R
{
    FileDelete, %A_LoopFileFullPath%
}





