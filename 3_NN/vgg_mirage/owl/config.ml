open Mirage

let main =
  foreign 
    ~packages:[package "owl"]
    (* ~packages:[package "owl_base"] *)
   "Vgg_owl.Main" job

let () = 
  register "Vgg_owl" [main]