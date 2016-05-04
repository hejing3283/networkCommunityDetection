#include "env.hh"
#include "mmsbinfer.hh"
#include "fastamm2.hh"
#include "sbm.hh"
#include "mmsbinferorig.hh"
#include "mmsbgen.hh"
#include "log.hh"
#include "mmsborig.hh"
#include "fastqueue.hh"
#include <stdlib.h>

#include <string>
#include <iostream>
#include <sstream>
#include <signal.h>

string Env::prefix = "";
Logger::Level Env::level = Logger::DEBUG;
FILE *Env::_plogf = NULL;
void usage();
void test();

Env *env_global = NULL;
volatile sig_atomic_t sig_handler_active = 0;

void
term_handler(int sig)
{
  if (env_global) {
    printf("\nGot signal. Saving model and groups.\n");
    fflush(stdout);
    env_global->terminate = 1;
  } else {
    signal(sig, SIG_DFL);
    raise(sig);
  }
}

int
main(int argc, char **argv)
{

  signal(SIGTERM, term_handler);

  bool run_gap = false;
  bool force_overwrite_dir = true;
  string datfname = "network.dat";

  //edits
  string gaufname = "attributes_gau.dat";
  string binfname = "attributes_bin.dat";
  //edits

  bool gen = false, ppc = false, lcstats = false;
  bool gml = false;
  bool findk = false;
  string label = "mmsb";
  uint32_t nthreads = 0;
  int i = 1;
  uint32_t n = 0, k = 0;

  // edit
  uint32_t dG = 0, dB = 0;
  // edit

  bool stratified = false, rnode = false, rpair = false;

  bool batch = false;
  bool online = false;
  bool nodelay = false;
  bool link_sampling = false;
  bool load = false;
  bool val_load = false;
  string val_file_location = "";
  bool test_load = false;
  string test_file_location = "";
  bool adamic_adar = false;
  string location = "";
  uint32_t scale = 1;
  bool disjoint = false;
  bool orig = false;
  bool massive = false;
  bool single = false;
  bool sparsek = false;
  bool logl = false;

  int itype = 0; // init type
  string eta_type = "uniform"; // "uniform", "fromdata", "sparse", "regular" or "dense"
  uint32_t rfreq = 1;
  bool accuracy = false;
  double stopthresh = 0.00001;

  double infthresh = 0;
  bool nonuniform = false;

  string ground_truth_fname = ""; // ground-truth communities file, if any
  bool nmi = false;
  bool bmark = false;
  bool randzeros = false;
  bool preprocess = false;
  bool strid = false;
  string groups_file = "";

  uint32_t max_iterations = 0;
  uint32_t use_validation_stop = true;
  double rand_seed = 0;

  double hol_ratio = 0.01;
  bool load_test_sets_opt = false;
  double link_thresh = 0.5;
  uint32_t lt_min_deg = 0;
  bool init_comm = false;
  string init_comm_fname = "";

  bool load_heldout_sets = false;

  if (argc == 1) {
    usage();
    exit(-1);
  }

  while (i <= argc - 1) {
    if (strcmp(argv[i], "-help") == 0) {
      usage();
      exit(0);
    } else if (strcmp(argv[i], "-file") == 0) {
      if (i + 1 > argc - 1) {
    	  fprintf(stderr, "+ insufficient arguments!\n");
    	  exit(-1);
      }
      datfname = string(argv[++i]);
     // edits
    }else if (strcmp(argv[i], "-fileGau") == 0) {
           if (i + 1 > argc - 1) {
         	  fprintf(stderr, "+ insufficient arguments!\n");
         	  exit(-1);
           }
           gaufname = string(argv[++i]);
    }else if (strcmp(argv[i], "-fileBin") == 0) {
               if (i + 1 > argc - 1) {
             	  fprintf(stderr, "+ insufficient arguments!\n");
             	  exit(-1);
               }
           binfname = string(argv[++i]);
    // edits
    } else if (strcmp(argv[i], "-stratified") == 0) {
      stratified = true;
      if (rfreq == 1)
	rfreq = 100;
    } else if (strcmp(argv[i], "-rnode") == 0) {
      rnode = true;
      if (rfreq == 1)
	rfreq = 100;
    } else if (strcmp(argv[i], "-n") == 0) {
      n = atoi(argv[++i]);
    } else if (strcmp(argv[i], "-k") == 0) {
      k = atoi(argv[++i]);
    } else if (strcmp(argv[i], "-dgau") == 0) {
      dG = atoi(argv[++i]);
    }else if (strcmp(argv[i], "-dbin") == 0) {
      dB = atoi(argv[++i]);
    }
    ++i;
  };

  assert (!(batch && online));

  Env env(n, k,
		  //edits
		  dG,dB,
		  //edits
		  massive, single, batch, stratified,
	  nodelay, rpair, rnode,
	  load, location,
	  val_load, val_file_location,
	  test_load, test_file_location,
	  load_test_sets_opt,
	  hol_ratio,
	  adamic_adar,
	  scale, disjoint,
	  force_overwrite_dir, datfname,
	  //edits
	  gaufname, binfname,
	  //edits
	  ppc, run_gap, gen, label, nthreads, itype, eta_type,
	  nmi, ground_truth_fname, rfreq,
	  accuracy, stopthresh, infthresh,
	  nonuniform, bmark, randzeros, preprocess,
	  strid, groups_file, logl,
	  max_iterations, use_validation_stop, rand_seed,
	  link_thresh, lt_min_deg,
	  init_comm, init_comm_fname,
	  link_sampling, gml, findk);

  env_global = &env;
  Network network(env);
  // if (!run_gap && gen) {
  //   if (orig) {
  //     info("+ generating mmsb network (with full blockmodel)\n");
  //     double alpha = (double)1.0 / env.k;
  //     MMSBOrig mmsborig(env, network);
  //     mmsborig.gen(alpha);
  //     exit(0);
  //   } else {
  //     info("+ generating mmsb network\n");
  //     double alpha = 0.05; //(double)1.0 / env.k;
  //     MMSBGen mmsbgen(env, network, false);
  //     mmsbgen.gen(alpha);
  //     exit(0);
  //   }
  // }
  if (network.read(datfname.c_str()) < 0) {
    fprintf(stderr, "error reading %s; quitting\n", datfname.c_str());
    return -1;
  }
  info("+ network: n = %d, ones = %d, singles = %d\n",
	  network.n(),
	  network.ones(), network.singles());

  env.n = network.n() - network.singles();

  //edits
  if (network.read_gau_attr(gaufname.c_str()) < 0) {
      fprintf(stderr, "error reading %s; quitting\n", gaufname.c_str());
      return -1;
    }
    info("+ gaussin attributes: dG = %d\n",network.dgau());

  if (network.read_bin_attr(binfname.c_str()) < 0) {
        fprintf(stderr, "error reading %s; quitting\n", binfname.c_str());
        return -1;
      }
      info("+ binary attributes: dG = %d\n", network.dbin());
  //edits


  if (stratified && rnode) {
    FastAMM2 fastamm2(env, network);
    info("+ running mmsb inference (with stratified random node option)\n");
    fastamm2.infer();
    exit(0);
  } else {
    MMSBInfer mmsb(env, network);
    info("+ running mmsb inference\n");
    mmsb.infer();
  }
}

void
usage()
{
  fprintf(stdout, "\nSVINET: fast stochastic variational inference of undirected networks\n"
	  "svinet [OPTIONS]\n"
	  "\t-help\t\tusage\n\n"
	  "\t-file <name>\tinput tab-separated file with a list of undirected links\n\n"
	  "\t-n <N>\t\tnumber of nodes in network\n\n"
	  "\t-k <K>\t\tnumber of communities\n\n"
	  "\t-batch\t\trun batch variational inference\n\n"
	  "\t-stratified\tuse stratified sampling\n\t * use with rpair or rnode options\n\n"
	  "\t-rnode\t\tinference using random node sampling\n\n"
	  );
  fflush(stdout);
}

void
test()
{
  FastQueue::static_initialize(100, 0.0001);
  FastQueue f;
  f.update(0, 10);
  f.update(1, 70);
  f.update(2, 15);
  f.update(3, 3);
  f.update(4, 1);

  double v = .0;
  f.find(0, v);
  printf("key:%d,val:%.3f\n", 0, v);
  f.find(1, v);
  printf("key:%d,val:%.3f\n", 1, v);
  f.find(2, v);
  printf("key:%d,val:%.3f\n", 2, v);
  v = .0;
  f.find(3, v);
  printf("key:%d,val:%.3f\n", 3, v);
  f.find(4, v);
  printf("key:%d,val:%.3f\n", 4, v);

  f.update(1, 80);
  f.update(1, 90);
  f.update(2, 30);

  exit(-1);
}
