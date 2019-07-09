module N = Owl_dense_ndarray.S
(* module N = Owl_base_dense_ndarray.S *)
module NL = Owl_neural_generic.Make (N)
open NL
open NL.Graph

let size = 32

let make_network img_size =
  input [|img_size;img_size;3|]
  |> conv2d [|3;3;3;32|] [|1;1|] ~act_typ:Activation.Relu
  |> conv2d [|3;3;32;32|] [|1;1|] ~act_typ:Activation.Relu ~padding:VALID
  |> max_pool2d [|2;2|] [|2;2|] ~padding:VALID
  |> conv2d [|3;3;32;64|] [|1;1|] ~act_typ:Activation.Relu
  |> conv2d [|3;3;64;64|] [|1;1|] ~act_typ:Activation.Relu ~padding:VALID
  |> max_pool2d [|2;2|] [|2;2|] ~padding:VALID
  |> fully_connected 512 ~act_typ:Activation.Relu
  |> linear 10 ~act_typ:Activation.Softmax
  |> get_network

let infer () = 
  let nn = make_network size in 
  Graph.init nn;
  let img_ppm = N.uniform [|1;size;size;3|] in

  let start_time = Unix.gettimeofday () in
  let result = Graph.model nn img_ppm in
  let end_time = Unix.gettimeofday () in
  Printf.printf "Execution time: %f seconds\n" (end_time -. start_time);
  
  result
  
let _ =
  infer () |> N.print ~max_col:5
