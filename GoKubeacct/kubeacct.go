package main

import(
	"context"
	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
	"github.com/prometheus/common/model"
	"time"

	//"encoding/json"
	"fmt"
	//"io/ioutil"
	"log"
	//"net/http"
	"os"
	"gopkg.in/alecthomas/kingpin.v2"
	clientapi "github.com/prometheus/client_golang/api"
	//"time"
)

var(
	app = kingpin.New("retrieve", "A command-line data retreiving application")
	debug = app.Flag("debug", "Enable debug mode").Bool()
	serverIP = app.Flag("server", "Server address").Default("127.0.0.1").IP()

	walltime = app.Command("walltime", "gathers data about total wallclock time per namespace")
	//walltimePeriod = walltime.Arg("period", "period for which data is gathered").Required().String()

	gpu = app.Command("gpu", "gathers data about total gpu usage per namespace")
	gpuPeriod = gpu.Arg("period", "period for which the data is gathered").Required().String()

	cpu = app.Command("cpu", "gathers data about total cpu usage per namespace")
	cpuPeriod = cpu.Arg("period", "period for which the data is gathered").Required().String()

	memory = app.Command("memory", "gathers data about the total memory usage per namespace")
	memoryPeriod = memory.Arg("period", "period for which the data is gathered").Required().String()

)

func main() {
	client, err := clientapi.NewClient(clientapi.Config{Address: "https://prometheus.nautilus.optiputer.net"})
	if err != nil {
		log.Printf("%v", err)
		return
	}

	q := v1.NewAPI(client)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	switch kingpin.MustParse(app.Parse(os.Args[1:])) {



	case walltime.FullCommand():


		if curVal, _, err := q.Query(ctx, "sum(node_namespace_pod:kube_pod_info:) by (namespace)", time.Now()); err != nil {
			log.Printf("Error: %v", err)
		} else {
			switch {
			case curVal.Type() == model.ValVector:
				vectorVal := curVal.(model.Vector)
				for _, elem := range vectorVal {
					fmt.Printf("Result: %s %f\n", elem.Metric["namespace"], float32(elem.Value))

				}
			}
		}

	case gpu.FullCommand():


		if curVal, _, err := q.Query(ctx, "increase(namespace_gpu_utilization[" + *gpuPeriod + "])", time.Now()); err != nil {
			log.Printf("Error: %v", err)
		} else {
			switch {
			case curVal.Type() == model.ValVector:
				vectorVal := curVal.(model.Vector)
				for _, elem := range vectorVal {
					fmt.Printf("Result: %s %f\n", elem.Metric["namespace_name"], float32(elem.Value))
				}
			}
		}


	case cpu.FullCommand():


		if curVal, _, err := q.Query(ctx, "increase(namespace_name:kube_pod_container_resource_requests_cpu_cores:sum[" + *cpuPeriod + "])", time.Now()); err != nil {
			log.Printf("Error: %v", err)
		} else {
			switch {
			case curVal.Type() == model.ValVector:
				vectorVal := curVal.(model.Vector)
				for _, elem := range vectorVal {
					fmt.Printf("Result: %s %f\n", elem.Metric["namespace_name"], float32(elem.Value))
				}
			}
		}


	case memory.FullCommand():


		if curVal, _, err := q.Query(ctx, "increase(namespace:container_memory_usage_bytes:sum[" + *memoryPeriod + "])", time.Now()); err != nil {
			log.Printf("Error: %v", err)
		} else {
			switch {
			case curVal.Type() == model.ValVector:
				vectorVal := curVal.(model.Vector)
				for _, elem := range vectorVal {
					fmt.Printf("Result: %s %f\n", elem.Metric["namespace_name"], float32(elem.Value))
				}
			}
		}
	}
}

