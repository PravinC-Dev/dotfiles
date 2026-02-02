local book_dir = vim.fn.expand("~/Irregular")

vim.api.nvim_create_autocmd("VimEnter", {
	callback = function()
		local cwd = vim.fn.getcwd()

		-- 1. Only run inside Irregular or its subdirectories
		if not cwd:match("^" .. vim.pesc(book_dir)) then
			return
		end

		-- 2. Find git repo root
		local git_root = vim.fn.systemlist("git rev-parse --show-toplevel")[1]
		if not git_root or git_root == "" then
			return
		end

		-- 3. CHECK CLEAN STATUS
		local status = vim.fn.systemlist("git -C " .. git_root .. " status --porcelain")
		if #status ~= 0 then
			vim.notify("Git pull skipped: working tree not clean", vim.log.levels.WARN)
			return
		end

		-- 4. Pull safely
		local result = vim.fn.system("git -C " .. git_root .. " pull --rebase --autostash 2>&1")

		-- 5. Notify result
		vim.schedule(function()
			if vim.v.shell_error == 0 then
				vim.notify("Git pull successful:\n" .. result, vim.log.levels.INFO)
			else
				vim.notify("Git pull failed:\n" .. result, vim.log.levels.ERROR)
			end
		end)
	end,
})
