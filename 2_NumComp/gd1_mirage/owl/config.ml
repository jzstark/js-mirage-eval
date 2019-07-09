open Mirage

let main =
  foreign 
    ~packages:[package "owl"]
    (* ~packages:[package "owl_base"; package "str"] *)
   "Gd_owl.GD" job

let () = 
  register "gd_owl" [main]

