open Mirage

let main =
  foreign 
    ~packages:[package "owl_base"]
    (* ~packages:[package "owl_base"] *)
   "Vgg_base.Main" job

let () = 
  register "Vgg_base" [main]