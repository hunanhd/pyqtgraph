(define read_file
  (lambda()
     (if (file-exists?".\hd.cas")
       (begin
        (read-case-data ".\hd.cas")
       )
      )
   )
)

(read_file)


(ti-menu-load-string "display/vector/velocity/velocity-magnitude")
