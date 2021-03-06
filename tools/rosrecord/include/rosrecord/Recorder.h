/*********************************************************************
* Software License Agreement (BSD License)
*
*  Copyright (c) 2008, Willow Garage, Inc.
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions
*  are met:
*
*   * Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*   * Redistributions in binary form must reproduce the above
*     copyright notice, this list of conditions and the following
*     disclaimer in the documentation and/or other materials provided
*     with the distribution.
*   * Neither the name of Willow Garage, Inc. nor the names of its
*     contributors may be used to endorse or promote products derived
*     from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
*  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
*  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
*  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
*  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
*  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
*  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
*  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*********************************************************************/

#ifndef IGNORE_ROSRECORD_DEPRECATED
#warning rosrecord/Recorder.h has been deprecated
#endif

#ifndef ROSRECORDRECORDER_H
#define ROSRECORDRECORDER_H

#include "ros/header.h"
#include "ros/time.h"
#include "ros/message.h"

#include <boost/thread/mutex.hpp>
#include <boost/iostreams/filtering_stream.hpp>

#include <fstream>
#include <iostream>
#include <map>

#include "rosbag/bag.h"

namespace ros
{
namespace record
{

typedef unsigned long long pos_t;

class Recorder
{
public:
  ROSCPP_DEPRECATED Recorder();
  virtual ~Recorder();

  bool open(const std::string& file_name, bool random_access=false);
  bool record(std::string topic_name, ros::Message::ConstPtr msg, ros::Time time);
  bool record(std::string topic_name, const ros::Message& msg, ros::Time time);
  void close();

  pos_t getOffset();

private:
  bool checkDisk();

private:
  rosbag::Bag bag_;

  bool logging_enabled_;

  boost::mutex  check_disk_mutex_;
  ros::WallTime check_disk_next_;
  ros::WallTime warn_next_;
};

}
}

#endif
