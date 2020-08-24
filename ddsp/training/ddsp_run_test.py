# Copyright 2020 The DDSP Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Tests for ddsp.training.ddsp_run."""

from unittest import mock

import ddsp_run
import tensorflow.compat.v2 as tf

class DownloadFromGstorageTest(tf.test.TestCase):

  @mock.patch('google.cloud.storage.Client.bucket')
  def test_bucket_name(self, bucket_function):
    """Check if proper bucket name is infered from path."""
    ddsp_run.download_from_gstorage(
        'gs://bucket-name/bucket/dir/some_file.gin',
        'local/path/some_file.gin')
    bucket_function.assert_called_with('bucket-name')


class HandleGstoragePathsTest(tf.test.TestCase):

  @mock.patch('ddsp_run.download_from_gstorage')
  def test_single_path_handling(self, download_from_gstorage_function):
    """Tests that function returns a single value if given single value."""
    path = ddsp_run.handle_gstorage_paths(
        'gs://bucket-name/bucket/dir/some_file.gin')
    download_from_gstorage_function.assert_called_once()
    self.assertEqual(path, 'some_file.gin')

  @mock.patch('ddsp_run.download_from_gstorage')
  def test_single_local_path_handling(self, download_from_gstorage_function):
    """Tests that function does nothing if given local file path."""
    path = ddsp_run.handle_gstorage_paths(
        'local_file.gin')
    download_from_gstorage_function.assert_not_called()
    self.assertEqual(path, 'local_file.gin')

  @mock.patch('ddsp_run.download_from_gstorage')
  def test_single_path_in_list_handling(self, download_from_gstorage_function):
    """Tests that function returns a single-element list if given one."""
    path = ddsp_run.handle_gstorage_paths(
        ['gs://bucket-name/bucket/dir/some_file.gin'])
    download_from_gstorage_function.assert_called_once()
    self.assertNotIsInstance(path, str)
    self.assertListEqual(path, ['some_file.gin'])

  @mock.patch('ddsp_run.download_from_gstorage')
  def test_more_paths_in_list_handling(self, download_from_gstorage_function):
    """Tests that function handle both local and gstorage paths in one list."""
    paths = ddsp_run.handle_gstorage_paths(
        ['gs://bucket-name/bucket/dir/first_file.gin',
         'local_file.gin',
         'gs://bucket-name/bucket/dir/second_file.gin'])
    self.assertEqual(download_from_gstorage_function.call_count, 2)
    download_from_gstorage_function.assert_has_calls(
        [mock.call('gs://bucket-name/bucket/dir/first_file.gin', mock.ANY),
         mock.call('gs://bucket-name/bucket/dir/second_file.gin', mock.ANY)])
    self.assertListEqual(
        paths,
        ['first_file.gin', 'local_file.gin', 'second_file.gin'])


if __name__ == '__main__':
  tf.test.main()
