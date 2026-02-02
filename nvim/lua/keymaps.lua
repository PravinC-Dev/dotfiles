local keymap = vim.keymap.set

-- Setup Keymaps Neovim --

-- Set leader
vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

-- Relativenumber toggle
keymap("n", "<leader>rn", ":set relativenumber!<CR>", { desc = "Relativenumber Toggle", silent = true }) -- Space r n

-- General clear highlights
keymap("n", "<Esc>", ":noh<CR>", { desc = "General Clear Highlights", silent = true })

-- Resize pane
keymap("n", "<A-=>", "<C-w>+", { desc = "Make Window Taller" }) -- Alt =
keymap("n", "<A-->", "<C-w>-", { desc = "Make Window Shorter" }) -- Alt -
keymap("n", "<A-,>", "<C-w>>", { desc = "Make Window Wider" }) -- Alt ,
keymap("n", "<A-.>", "<C-w><", { desc = "Make Window Narrower" }) -- Alt .

-- Move on pane
-- keymap("n", "<C-K>", "<C-w>k", { desc = "Move To Upper Pane" })     -- Ctrl k
-- keymap("n", "<C-J>", "<C-w>j", { desc = "Move To Bottom Pane" })    -- Ctrl j
-- keymap("n", "<C-H>", "<C-w>h", { desc = "Move To Left Pane" })      -- Ctrl h
-- keymap("n", "<C-L>", "<C-w>l", { desc = "Move To Right Pane" })     -- Ctrl l

-- Window navigation with <leader> + h/j/k/l
vim.keymap.set("n", "<leader>h", "<C-w>h", { silent = true })
vim.keymap.set("n", "<leader>j", "<C-w>j", { silent = true })
vim.keymap.set("n", "<leader>k", "<C-w>k", { silent = true })
vim.keymap.set("n", "<leader>l", "<C-w>l", { silent = true })

-- Set move line
keymap("n", "<A-Up>", ":m .-2<CR>", { desc = "Move Line Up (Normal mode)", silent = true }) -- Alt Up
keymap("n", "<A-Down>", ":m .+1<CR>", { desc = "Move Line Down (Normal mode)", silent = true }) -- Alt Down
keymap("v", "<A-Up>", ":m '<-2<CR>gv=gv", { desc = "Move Line(s) Up (Visual mode)", silent = true }) -- Alt Up
keymap("v", "<A-Down>", ":m '>+1<CR>gv=gv", { desc = "Move Line(s) Down (Visual mode)", silent = true }) -- Alt Down

-- Indentation
keymap("n", "<Tab>", ">>", { desc = "Indent Line (Normal mode)" }) -- Tab
keymap("n", "<S-Tab>", "<<", { desc = "Unindent Line (Normal mode)" }) -- Shift Tab
keymap("v", "<Tab>", ">gv", { desc = "Indent Selection (Visual mode)" }) -- Tab
keymap("v", "<S-Tab>", "<gv", { desc = "Unindent Selection (Visual mode)" }) -- Shift Tab

-- Cord.nvim setup
vim.keymap.set("n", "<leader>rp", function()
	require("cord").setup(require("user.cord"))
end, { desc = "Start Cord presence" })

vim.keymap.set("n", "<leader>rd", function()
	vim.cmd("Cord shutdown")
end, { desc = "Shutdown Cord presence" })

-- Wrap in asterisk
vim.keymap.set("x", "<leader>i", 'c*<C-r>"*', { noremap = true })

--Bold
vim.keymap.set("x", "<C-b>", 'c**<C-r>"**', { noremap = true })

--Copy the rendered text from markdown instead of raw code
vim.keymap.set('v', '<leader>y',
  [[:w !pandoc -f markdown -t html | wl-copy --type text/html<CR><CR>]],
  { noremap = true, silent = true, desc = "Copy Markdown as rendered HTML" }
)

--Mapping leader+d to send the text to shadow realm instead of saving it to clipboard
vim.keymap.set("v", "<leader>d", '"_d', { desc = "Delete without yanking" })
vim.keymap.set("n", "<leader>d", '"_d', { desc = "Delete without yanking" })


--Text movement
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

