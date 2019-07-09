module M = Owl_dense_ndarray.S

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

let v = M.empty dims

let wrap_fun () =
  begin
    for rep = 0 to 10 do
      for axis = 0 to rank - 1 do
        let _ = M.fold ~axis Pervasives.(+.) 0. v in
        ()
      done
    done
  end

let _ = time_function wrap_fun