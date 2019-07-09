open Owl_base
module A = Owl_algodiff_generic.Make (Owl_base_dense_ndarray.S)
open A

let rec desc ?(eta=F 0.01) ?(eps=1e-6) f x =
  let g = (diff f) x in
  if (unpack_flt (Maths.abs g)) < eps then x
  else desc ~eta ~eps f Maths.(x - eta * g)


let main () =
  let f = Maths.sin in
  let init = Owl_base.Stats.uniform 0. 10. in
  let start_time = Unix.gettimeofday () in
  let y = desc f (F init) in
  let end_time = Unix.gettimeofday () in
  Printf.printf "Execution time: %f seconds\n" (end_time -. start_time);  
  Owl_log.info "argmin f(x) = %g" (unpack_flt y)

module GD = struct
  let start = main (); Lwt.return_unit
end