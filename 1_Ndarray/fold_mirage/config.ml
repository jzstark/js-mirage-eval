open Mirage

let key =
  let doc = Key.Arg.info ~doc:"Ndarray Dims" ["params"] in
  Key.(create "params" Arg.(opt string "100 100" doc))

let main =
  foreign 
    ~keys:[Key.abstract key]
    ~packages:[package "owl_base"; package "str"]
    (* ~packages:[package "owl"; package "str"] *)
   "Unikernel.FOLD" (time @-> job)

let () = 
  register "fold_base" [main $ default_time]
