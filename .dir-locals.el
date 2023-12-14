;;; Directory Local Variables            -*- no-byte-compile: t -*-
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((eval . (progn
                   ;; install or activate the development environment
                   ;; (requires pyvenv-tracking-mode)
                   (set (make-local-variable 'my-project)
                        (locate-dominating-file default-directory ".dir-locals.el"))
                   (set (make-local-variable 'my-project-venv)
                        (concat my-project ".venv"))
                   (if (not (file-exists-p my-project-venv))
                       (let ((cwd default-directory))
                         (cd my-project)
                         (async-shell-command "make dev-infra")
                         (cd cwd)
                         (message "Please re-open this file/directory after the \"make dev-infra\" command finishes."))
                     ;; must be set project-wide to pre-commit work
                     (set (make-local-variable 'pyvenv-activate)
                          my-project-venv))))))
 (python-mode . ((eval . (progn
                           ;; sort imports, then style code
                           (add-hook 'before-save-hook #'py-isort-before-save nil t)
                           (add-hook 'before-save-hook #'elpy-black-fix-code nil t))))))
