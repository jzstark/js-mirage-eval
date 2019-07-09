module M = Owl_base_dense_ndarray.S

let time_function f =
  let start_time = Unix.gettimeofday () in
  let result = f () in
  let end_time = Unix.gettimeofday () in
  Printf.printf "Execution time: %f seconds\n" (end_time -. start_time);
  result

let _ = Printf.printf "Evaluating map operation\n"

let rank = (Array.length Sys.argv) - 1

let _ =
  if (rank <= 0)
  then failwith "ERROR! Must provide the dimensions of the Ndarray."

let dims = Array.init rank (fun i -> int_of_string Sys.argv.(i + 1))
let _ = Printf.printf "Evaluating Ndarray of rank %d with dims: [" rank
let _ = Array.iter (fun d -> Printf.printf "%d " d) dims
let _ = Printf.printf "]\n"

let f0 = (fun _ -> 0.)
let f1 = (fun _ -> 1.)
let f2 = (fun x -> x +. 11.)
let f3 = (fun x -> x *. 2.)
let f4 = (fun x -> x /. 2.)

let funs = [f0; f1; f2; f3; f4]

let v = ref (M.empty dims)

let wrap_fun () =
  begin
    for rep = 0 to 10 do
      List.iter (fun f -> v := M.map f !v) funs
    done
  end

let _ = time_function wrap_fun