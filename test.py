import unittest

from sim_runner.core import runner


class TestSimRunner(unittest.TestCase):
    """
    Integration tests for sim_runner
    """
    def test_local_dry(self):
        """
        Test local job creation in dry run mode with producing the parametric scans
        """
        config_file_name = './examples/test_local_dry.toml'
        verbosity = 0
        runner.run(config_file_name, verbosity)

    def test_sge(self):
        """
        Test SGE/PBS job creation
        """
        test_job = """#!/bin/bash
#PBS -l walltime=167:59:59
#PBS -l vmem=2200mb
#PBS -l nodes=1:ppn=1
#PBS -q qlong
#PBS -o /tmp/sim_runner//log/job_sim_telarray_gamma_1.log
#PBS -e /tmp/sim_runner//error/job_sim_telarray_gamma_1.err

/opt/sim_telarray/bin/sim_telarray -I/tmp/sim_telarray-config -c /tmp/sim_telarray-config/config.cfg -DNUM_TELESCOPES=1 -C min_photoelectrons=-1 -C min_photons=-1 -C only_triggered_telescopes=0 -C only_triggered_arrays=0 -C maximum_events=100 -C ignore_telescopes=all:-1 -C maximum_telescopes=7 -C random_state=auto -C show=all -C telescope_phi=174.6805 -C telescope_zenith_angle=20 -C nsb_scaling_factor=2 -C pedestal_events=10 -C asum_threshold=1000 -h ./test/output//hist/dummy100000.hdata -o ./test/output/dummy100000.simtel.gz ./examples/data//dummy100000.corsika.gz 2>&1 > ./test/output//log/dummy100000.log
"""
        config_file_name = './examples/test_sge.toml'
        verbosity = 0
        runner.run(config_file_name, verbosity)
        job_file = open('/tmp/sim_runner/job_sim_telarray_gamma_1.job', 'r')
        job_content = job_file.read()
        job_file.close()
        self.assertEqual(job_content.rstrip(), test_job.rstrip())

    def test_slurm(self):
        """
        Test SLURM job creation
        """
        test_job = """#!/bin/bash
#SBATCH --partition=mono-shared-EL7
#SBATCH --time=167:59:59
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2200 # in MB
#SBATCH --output=/tmp/sim_runner//log/job_sim_telarray_gamma_1.log
#SBATCH --error=/tmp/sim_runner//error/job_sim_telarray_gamma_1.err

srun /opt/sim_telarray/bin/sim_telarray -I/tmp/sim_telarray-config -c /tmp/sim_telarray-config/config.cfg -DNUM_TELESCOPES=1 -C min_photoelectrons=-1 -C min_photons=-1 -C only_triggered_telescopes=0 -C only_triggered_arrays=0 -C maximum_events=100 -C ignore_telescopes=all:-1 -C maximum_telescopes=7 -C random_state=auto -C show=all -C telescope_phi=174.6805 -C telescope_zenith_angle=20 -C nsb_scaling_factor=2 -C pedestal_events=10 -C asum_threshold=1000 -h ./test/output//hist/dummy100000.hdata -o ./test/output/dummy100000.simtel.gz ./examples/data//dummy100000.corsika.gz 2>&1 > ./test/output//log/dummy100000.log
"""
        config_file_name = './examples/test_slurm.toml'
        verbosity = 0
        runner.run(config_file_name, verbosity)
        job_file = open('/tmp/sim_runner/job_sim_telarray_gamma_1.job', 'r')
        job_content = job_file.read()
        job_file.close()
        self.assertEqual(job_content.rstrip(), test_job.rstrip())

    def test_local_run(self):
        """
        Test local job creation and running
        """
        config_file_name = './examples/test_local.toml'
        verbosity = 0
        runner.run(config_file_name, verbosity)

    def test_local_dry_run_corsika(self):
        """
        Test local corsika job creation (dry running)
        """
        config_file_name = './examples/test_local_corsika_dry.toml'
        verbosity = 0
        runner.run(config_file_name, verbosity)

if __name__ == '__main__':
    unittest.main()
