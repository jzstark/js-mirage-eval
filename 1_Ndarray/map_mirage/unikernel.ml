(* The code has to be modified to be passed in paramters:
 * 1. change the coding fo parameters passing;
 * 2. add the time-related module (?)
 * 3. add key in config.ml
 * 4. put all the code under "start"
 * 
 * Usage: ./map_mirage.exe --params="100 100"
 *)

module M = Owl_base_dense_ndarray.S
(* module M = Owl_dense_ndarray.S *)
let time_function f =
  let start_time = Unix.gettimeofday () in
  let result = f () in
  let end_time = Unix.gettimeofday () in
  Printf.printf "Execution time: %f seconds\n" (end_time -. start_time);
  result


module MAP (Time : Mirage_time_lwt.S) = struct

let start _time = 

let params = Key_gen.params () in

let _ = Printf.printf "Evaluating map operation\n" in 

let dims = Str.split (Str.regexp " ") params 
  |> List.map int_of_string
  |> Array.of_list
in 

let rank = Array.length dims in

let _ =
  if (rank <= 0)
  then failwith "ERROR! Must provide the dimensions of the Ndarray."
in

let _ = Printf.printf "Evaluating Ndarray of rank %d with dims: [" rank in
let _ = Array.iter (fun d -> Printf.printf "%d " d) dims in
let _ = Printf.printf "]\n" in


let f0 = (fun _ -> 0.) in
let f1 = (fun _ -> 1.) in
let f2 = (fun x -> x +. 11.) in
let f3 = (fun x -> x *. 2.) in
let f4 = (fun x -> x /. 2.) in

let funs = [f0; f1; f2; f3; f4] in

let v = ref (M.empty dims) in

let wrap_fun () =
  begin
    for _ = 0 to 10 do
      List.iter (fun f -> v := M.map f !v) funs
    done
  end
in

let main () = time_function wrap_fun in

main ();
Lwt.return_unit

end
