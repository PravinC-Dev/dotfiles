-- Automatically regenerate tags on saving Rust files
vim.api.nvim_create_autocmd("BufWritePost", {
	pattern = "*.rs",
	callback = function()
		vim.fn.system("ctags -R --languages=Rust --exclude=target -f tags")
	end,
})

vim.api.nvim_create_autocmd("QuickFixCmdPost", {
	pattern = "make",
	callback = function()
		vim.cmd("cwindow")
	end,
})

-- Auto-start Cord on each nvim startup
vim.api.nvim_create_autocmd("VimEnter", {
	callback = function()
		require("cord").setup(require("user.cord"))
	end,
})

-- Markdown formattings
vim.api.nvim_create_autocmd("FileType", {
  pattern = "markdown",
  callback = function()
    local buf_dir = vim.fn.fnamemodify(
      vim.api.nvim_buf_get_name(0),
      ":p:h"
    )

    vim.opt_local.wrap = true
    vim.opt_local.linebreak = true
    vim.opt_local.breakindent = true
    vim.opt_local.conceallevel = 2
    vim.opt_local.spell = true
    vim.opt_local.textwidth = 0

    vim.opt_local.spellfile =
      vim.fn.expand("~/.config/nvim/spell/en.utf-8.add")
      .. ","
      .. buf_dir
      .. "/.spell.add"
  end,
})

