open Mirage

let main =
  foreign 
    ~packages:[package "owl_base"]
    (* ~packages:[package "owl_base"] *)
   "Sqnet_base.Main" job

let () = 
  register "Sqnet_base" [main]