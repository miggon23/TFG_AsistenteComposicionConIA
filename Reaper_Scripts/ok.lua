
-- -- Verificar si el comando ya está registrado
local existingCommandID = reaper.NamedCommandLookup("demo.py")
local addSuccess = 0

local script_path = debug.getinfo(1, "S").source:sub(2)

local demoPath = script_path:match("^(.*)[\\/]") .. "/demo.py"
--reaper.ShowConsoleMsg("Ruta abs al script" .. demoPath)

if (existingCommandID == 0) then
    -- El comando no está registrado, añadirlo
    addSuccess = reaper.AddRemoveReaScript(true, 0, demoPath, true)

    if addSuccess == 0 then
        reaper.ShowConsoleMsg("Error al añadir el comando.\n")
    end
else
    addSuccess = existingCommandID
end
-- Tras añadir el comando con reaper.AddRemoveReaScript, llamar al propio comando
-- The commandID returned, might change, when adding this script into another Reaper-installation.
-- To be sure to use the right command-id, use ReverseNamedCommandLookup() to get the ActionCommandID, which will never change, until you remove the script.
--reaper.Main_OnCommand(reaper.NamedCommandLookup("_RSf66020190561c765fcfea95533ef6011bc692add"), 0)
reaper.Main_OnCommand(addSuccess, 0)

-- Play🌻
reaper.Main_OnCommand(40044, 0)