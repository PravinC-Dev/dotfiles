return {
	"nvim-lualine/lualine.nvim",
	dependencies = {
		"nvim-tree/nvim-web-devicons",
	},

	config = function()
		-- --------------------------------------------------
		-- Markdown helpers
		-- --------------------------------------------------
		local function is_markdown()
			return vim.bo.filetype == "markdown" or vim.bo.filetype == "asciidoc"
		end

		-- --------------------------------------------------
		-- Visual selection helpers (lualine-safe)
		-- --------------------------------------------------
		local function is_visual()
			return vim.fn.mode():match("[vV\22]") ~= nil
		end

		local function get_visual_selection()
			local start_pos = vim.fn.getpos("'<")
			local end_pos = vim.fn.getpos("'>")

			if start_pos[2] == 0 or end_pos[2] == 0 then
				return nil
			end

			local lstart, cstart = start_pos[2], start_pos[3]
			local lend, cend = end_pos[2], end_pos[3]

			if lstart > lend or (lstart == lend and cstart > cend) then
				lstart, lend = lend, lstart
				cstart, cend = cend, cstart
			end

			local lines = vim.fn.getline(lstart, lend)
			if #lines == 0 then
				return nil
			end

			lines[1] = string.sub(lines[1], cstart)
			lines[#lines] = string.sub(lines[#lines], 1, cend)

			return table.concat(lines, "\n")
		end

		local function selection_count()
			local wc = vim.fn.wordcount()
			if not wc.visual_words or wc.visual_words == 0 then
				return ""
			end

			return string.format("%d chars | %d words", wc.visual_chars, wc.visual_words)
		end

		local function document_wordcount()
			local wc = vim.fn.wordcount().words
			return wc > 0 and (wc .. " words") or ""
		end

		local function document_charcount()
			local bufnr = vim.api.nvim_get_current_buf()
			local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
			local text = table.concat(lines, "\n")
			local chars = vim.fn.strchars(text)
			return chars > 0 and (chars .. " chars") or ""
		end

		-- --------------------------------------------------
		-- Lualine setup
		-- --------------------------------------------------
		require("lualine").setup({
			options = {
				theme = "auto",
				icons_enabled = true,
				component_separators = "",
				section_separators = "",
				disabled_filetypes = { "vim-plug", "Outline" },
				always_divide_middle = true,
				globalstatus = true,
			},

			sections = {
				lualine_a = { "mode" },
				lualine_b = { "branch", "diff" },
				lualine_c = {
					{
						"filename",
						path = 0,
						symbols = {
							modified = " ",
							readonly = " ",
							unnamed = "[No Name]",
							newfile = "[New]",
						},
					},
				},

				lualine_x = {
					"diagnostics",
					{ "filetype", colored = true },

					-- Selection-aware counts
					{
						selection_count,
						cond = function()
							return is_markdown() and is_visual()
						end,
					},
					{
						document_charcount,
						cond = function()
							return is_markdown() and not is_visual()
						end,
					},
					{
						document_wordcount,
						cond = function()
							return is_markdown() and not is_visual()
						end,
					},

					"encoding",
					{ "fileformat", icons_enabled = false },
				},

				lualine_y = { "progress" },
				lualine_z = { "location" },
			},

			inactive_sections = {
				lualine_a = {},
				lualine_b = {},
				lualine_c = { "filename" },
				lualine_x = { "location" },
				lualine_y = {},
				lualine_z = {},
			},

			extensions = { "fzf", "nvim-tree", "nvim-dap-ui" },
		})
	end,
}
