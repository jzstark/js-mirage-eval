open Mirage

let main =
  foreign 
    ~packages:[package "owl_base"]
    (* ~packages:[package "owl_base"; package "str"] *)
   "Gd_base.GD" job

let () = 
  register "gd_base" [main]

