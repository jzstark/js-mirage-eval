open Mirage

let main =
  foreign 
    ~packages:[package "owl"]
    (* ~packages:[package "owl_base"] *)
   "Sqnet_owl.Main" job

let () = 
  register "Sqnet_owl" [main]